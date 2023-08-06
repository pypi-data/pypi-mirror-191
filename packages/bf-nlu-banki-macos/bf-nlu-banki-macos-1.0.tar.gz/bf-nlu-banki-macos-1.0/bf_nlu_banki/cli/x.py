import argparse
import asyncio
import importlib.util
import logging
from multiprocessing.process import BaseProcess
from multiprocessing import get_context
from packaging import version
from pathlib import Path
import os
import signal
import sys
import traceback
from typing import Iterable, List, Optional, Text, Tuple, Union

import aiohttp
from bf_nlu_banki.exceptions import MissingDependencyException
import ruamel.yaml as yaml

from bf_nlu_banki import telemetry
from bf_nlu_banki.cli import SubParsersAction
from bf_nlu_banki.cli.arguments import x as arguments
import bf_nlu_banki.cli.utils
from bf_nlu_banki.constants import (
    DEFAULT_LOG_LEVEL_bf_nlu_banki_X,
    DEFAULT_bf_nlu_banki_PORT,
    DEFAULT_bf_nlu_banki_X_PORT,
)
from bf_nlu_banki.shared.constants import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_CREDENTIALS_PATH,
    DEFAULT_DOMAIN_PATH,
    DEFAULT_ENDPOINTS_PATH,
    DOCS_BASE_URL_bf_nlu_banki_X,
)
from bf_nlu_banki.core.utils import AvailableEndpoints
from bf_nlu_banki.shared.exceptions import bf_nlu_bankiXTermsError
import bf_nlu_banki.shared.utils.cli
import bf_nlu_banki.shared.utils.io
import bf_nlu_banki.utils.common
from bf_nlu_banki.utils.endpoints import EndpointConfig
import bf_nlu_banki.utils.io

logger = logging.getLogger(__name__)

DEFAULT_EVENTS_DB = "events.db"


def add_subparser(
    subparsers: SubParsersAction, parents: List[argparse.ArgumentParser]
) -> None:
    """Add all bf_nlu_banki x parsers.

    Args:
        subparsers: subparser we are going to attach to
        parents: Parent parsers, needed to ensure tree structure in argparse
    """
    x_parser_args = {
        "parents": parents,
        "conflict_handler": "resolve",
        "formatter_class": argparse.ArgumentDefaultsHelpFormatter,
    }

    if is_bf_nlu_banki_x_installed():
        # we'll only show the help msg for the command if bf_nlu_banki X is actually installed
        x_parser_args["help"] = "Starts the bf_nlu_banki X interface."

    shell_parser = subparsers.add_parser("x", **x_parser_args)
    shell_parser.set_defaults(func=bf_nlu_banki_x)

    arguments.set_x_arguments(shell_parser)


def _bf_nlu_banki_service(
    args: argparse.Namespace,
    endpoints: AvailableEndpoints,
    bf_nlu_banki_x_url: Optional[Text] = None,
    credentials_path: Optional[Text] = None,
) -> None:
    """Starts the bf_nlu_banki application."""
    from bf_nlu_banki.core.run import serve_application

    # needs separate logging configuration as it is started in its own process
    bf_nlu_banki.utils.common.configure_logging_and_warnings(args.loglevel)
    bf_nlu_banki.utils.io.configure_colored_logging(args.loglevel)

    if not credentials_path:
        credentials_path = _prepare_credentials_for_bf_nlu_banki_x(
            args.credentials, bf_nlu_banki_x_url=bf_nlu_banki_x_url
        )

    serve_application(
        endpoints=endpoints,
        port=args.port,
        credentials=credentials_path,
        cors=args.cors,
        auth_token=args.auth_token,
        enable_api=True,
        jwt_secret=args.jwt_secret,
        jwt_method=args.jwt_method,
        ssl_certificate=args.ssl_certificate,
        ssl_keyfile=args.ssl_keyfile,
        ssl_ca_file=args.ssl_ca_file,
        ssl_password=args.ssl_password,
    )


def _prepare_credentials_for_bf_nlu_banki_x(
    credentials_path: Optional[Text], bf_nlu_banki_x_url: Optional[Text] = None
) -> Text:
    credentials_path = str(
        bf_nlu_banki.cli.utils.get_validated_path(
            credentials_path, "credentials", DEFAULT_CREDENTIALS_PATH, True
        )
    )
    if credentials_path:
        credentials = bf_nlu_banki.shared.utils.io.read_config_file(credentials_path)
    else:
        credentials = {}

    # this makes sure the bf_nlu_banki X is properly configured no matter what
    if bf_nlu_banki_x_url:
        credentials["bf_nlu_banki"] = {"url": bf_nlu_banki_x_url}
    dumped_credentials = yaml.dump(credentials, default_flow_style=False)
    tmp_credentials = bf_nlu_banki.utils.io.create_temporary_file(dumped_credentials, "yml")

    return tmp_credentials


def _overwrite_endpoints_for_local_x(
    endpoints: AvailableEndpoints, bf_nlu_banki_x_token: Text, bf_nlu_banki_x_url: Text
) -> None:
    endpoints.model = _get_model_endpoint(endpoints.model, bf_nlu_banki_x_token, bf_nlu_banki_x_url)
    endpoints.event_broker = _get_event_broker_endpoint(endpoints.event_broker)


def _get_model_endpoint(
    model_endpoint: Optional[EndpointConfig], bf_nlu_banki_x_token: Text, bf_nlu_banki_x_url: Text
) -> EndpointConfig:
    # If you change that, please run a test with bf_nlu_banki X and speak to the bot
    default_bf_nlu_bankix_model_server_url = f"{bf_nlu_banki_x_url}/models/tags/production"

    model_endpoint = model_endpoint or EndpointConfig()

    # Checking if endpoint.yml has existing url, if so give
    # warning we are overwriting the endpoint.yml file.
    custom_url = model_endpoint.url

    if custom_url and custom_url != default_bf_nlu_bankix_model_server_url:
        logger.info(
            f"Ignoring url '{custom_url}' from 'endpoints.yml' and using "
            f"'{default_bf_nlu_bankix_model_server_url}' instead."
        )

    custom_wait_time_pulls = model_endpoint.kwargs.get("wait_time_between_pulls")
    return EndpointConfig(
        default_bf_nlu_bankix_model_server_url,
        token=bf_nlu_banki_x_token,
        wait_time_between_pulls=custom_wait_time_pulls or 2,
    )


def _get_event_broker_endpoint(
    event_broker_endpoint: Optional[EndpointConfig],
) -> EndpointConfig:
    import questionary

    default_event_broker_endpoint = EndpointConfig(
        type="sql", dialect="sqlite", db=DEFAULT_EVENTS_DB
    )
    if not event_broker_endpoint:
        return default_event_broker_endpoint
    elif not _is_correct_event_broker(event_broker_endpoint):
        bf_nlu_banki.shared.utils.cli.print_error(
            f"bf_nlu_banki X currently only supports a SQLite event broker with path "
            f"'{DEFAULT_EVENTS_DB}' when running locally. You can deploy bf_nlu_banki X "
            f"with Docker ({DOCS_BASE_URL_bf_nlu_banki_X}/installation-and-setup/"
            f"docker-compose-quick-install/) if you want to use other event broker "
            f"configurations."
        )
        continue_with_default_event_broker = questionary.confirm(
            "Do you want to continue with the default SQLite event broker?"
        ).ask()

        if not continue_with_default_event_broker:
            sys.exit(0)

        return default_event_broker_endpoint
    else:
        return event_broker_endpoint


def _is_correct_event_broker(event_broker: EndpointConfig) -> bool:
    return all(
        [
            event_broker.type == "sql",
            event_broker.kwargs.get("dialect", "").lower() == "sqlite",
            event_broker.kwargs.get("db") == DEFAULT_EVENTS_DB,
        ]
    )


def start_bf_nlu_banki_for_local_bf_nlu_banki_x(
    args: argparse.Namespace, bf_nlu_banki_x_token: Text
) -> BaseProcess:
    """Starts the bf_nlu_banki X API with bf_nlu_banki as a background process."""
    credentials_path, endpoints_path = _get_credentials_and_endpoints_paths(args)
    endpoints = AvailableEndpoints.read_endpoints(endpoints_path)

    bf_nlu_banki_x_url = f"http://localhost:{args.bf_nlu_banki_x_port}/api"
    _overwrite_endpoints_for_local_x(endpoints, bf_nlu_banki_x_token, bf_nlu_banki_x_url)

    vars(args).update(
        dict(
            nlu_model=None,
            cors="*",
            auth_token=args.auth_token,
            enable_api=True,
            endpoints=endpoints,
        )
    )

    ctx = get_context("spawn")
    p = ctx.Process(
        target=_bf_nlu_banki_service,
        args=(args, endpoints, bf_nlu_banki_x_url, credentials_path),
        daemon=True,
    )
    p.start()
    return p


def is_bf_nlu_banki_x_installed() -> bool:
    """Check if bf_nlu_banki X is installed."""

    # we could also do something like checking if `import bf_nlu_bankix` works,
    # the issue with that is that it actually does import the package and this
    # takes some time that we don't want to spend when booting the CLI
    return importlib.util.find_spec("bf_nlu_bankix") is not None


def generate_bf_nlu_banki_x_token(length: int = 16) -> Text:
    """Generate a hexadecimal secret token used to access the bf_nlu_banki X API.

    A new token is generated on every `bf_nlu_banki x` command.
    """

    from secrets import token_hex

    return token_hex(length)


def _configure_logging(args: argparse.Namespace) -> None:
    from bf_nlu_banki.core.utils import configure_file_logging
    from bf_nlu_banki.utils.common import configure_logging_and_warnings

    log_level = args.loglevel or DEFAULT_LOG_LEVEL_bf_nlu_banki_X

    if isinstance(log_level, str):
        log_level = logging.getLevelName(log_level)

    logging.basicConfig(level=log_level)
    bf_nlu_banki.utils.io.configure_colored_logging(args.loglevel)

    configure_logging_and_warnings(
        log_level, warn_only_once=False, filter_repeated_logs=False
    )
    configure_file_logging(logging.root, args.log_file, False)

    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("engineio").setLevel(logging.WARNING)
    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.getLogger("socketio").setLevel(logging.ERROR)

    if not log_level == logging.DEBUG:
        logging.getLogger().setLevel(logging.WARNING)
        logging.getLogger("py.warnings").setLevel(logging.ERROR)


def is_bf_nlu_banki_project_setup(args: argparse.Namespace, project_path: Text) -> bool:
    """Checks if `project_path` contains a valid bf_nlu_banki Open Source project.

    Args:
        args: Command-line arguments.
        project_path: Path to the possible bf_nlu_banki Open Source project.

    Returns:
        `True` if `project_path` is a valid bf_nlu_banki Open Source project, `False` otherwise.
    """
    config_path = _get_config_path(args)
    domain_path = _get_domain_path(args)

    mandatory_files = [config_path, domain_path]

    for f in mandatory_files:
        if not os.path.exists(os.path.join(project_path, f)):
            return False

    return True


def _validate_bf_nlu_banki_x_start(args: argparse.Namespace, project_path: Text) -> None:
    if not is_bf_nlu_banki_x_installed():
        bf_nlu_banki.shared.utils.cli.print_error_and_exit(
            "bf_nlu_banki X is not installed. The `bf_nlu_banki x` "
            "command requires an installation of bf_nlu_banki X. "
            "Instructions on how to install bf_nlu_banki X can be found here: "
            "https://bf_nlu_banki.com/docs/bf_nlu_banki-x/."
        )

    if args.port == args.bf_nlu_banki_x_port:
        bf_nlu_banki.shared.utils.cli.print_error_and_exit(
            "The port for bf_nlu_banki X '{}' and the port of the bf_nlu_banki server '{}' are the "
            "same. We need two different ports, one to run bf_nlu_banki X (e.g. delivering the "
            "UI) and another one to run a normal bf_nlu_banki server.\nPlease specify two "
            "different ports using the arguments '--port' and '--bf_nlu_banki-x-port'.".format(
                args.bf_nlu_banki_x_port, args.port
            )
        )

    if not is_bf_nlu_banki_project_setup(args, project_path):
        bf_nlu_banki.shared.utils.cli.print_error_and_exit(
            "This directory is not a valid bf_nlu_banki project. Use 'bf_nlu_banki init' "
            "to create a new bf_nlu_banki project or switch to a valid bf_nlu_banki project "
            "directory (see "
            "https://bf_nlu_banki.com/docs/bf_nlu_banki/command-line-interface#bf_nlu_banki-init)."
        )

    domain_path = _get_domain_path(args)
    _validate_domain(os.path.join(project_path, domain_path))

    if args.data and not os.path.exists(args.data):
        bf_nlu_banki.shared.utils.cli.print_warning(
            "The provided data path ('{}') does not exists. bf_nlu_banki X will start "
            "without any training data.".format(args.data)
        )


def _validate_domain(domain_path: Text) -> None:
    from bf_nlu_banki.shared.core.domain import Domain, InvalidDomain

    try:
        Domain.load(domain_path)
    except InvalidDomain as e:
        bf_nlu_banki.shared.utils.cli.print_error_and_exit(
            "The provided domain file could not be loaded. " "Error: {}".format(e)
        )


def bf_nlu_banki_x(args: argparse.Namespace) -> None:
    from bf_nlu_banki.cli.utils import signal_handler

    signal.signal(signal.SIGINT, signal_handler)

    _configure_logging(args)

    if version.parse(bf_nlu_banki.version.__version__) >= version.parse("3.0.0"):
        bf_nlu_banki.shared.utils.io.raise_warning(
            f"Your version of bf_nlu_banki '{bf_nlu_banki.version.__version__}' is currently "
            f"not supported by bf_nlu_banki X. Running `bf_nlu_banki x` CLI command with bf_nlu_banki "
            f"version higher or equal to 3.0.0 will result in errors.",
            UserWarning,
        )

    if args.production:
        run_in_production(args)
    else:
        run_locally(args)


async def _pull_runtime_config_from_server(
    config_endpoint: Optional[Text],
    attempts: int = 60,
    wait_time_between_pulls: float = 5,
    keys: Iterable[Text] = ("endpoints", "credentials"),
) -> List[Text]:
    """Pull runtime config from `config_endpoint`.

    Returns a list of paths to yaml dumps, each containing the contents of one of
    `keys`.
    """
    while attempts:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(config_endpoint) as resp:
                    if resp.status == 200:
                        rjs = await resp.json()
                        try:
                            return [
                                bf_nlu_banki.utils.io.create_temporary_file(rjs[k])
                                for k in keys
                            ]
                        except KeyError as e:
                            bf_nlu_banki.shared.utils.cli.print_error_and_exit(
                                "Failed to find key '{}' in runtime config. "
                                "Exiting.".format(e)
                            )
                    else:
                        logger.debug(
                            "Failed to get a proper response from remote "
                            "server. Status Code: {}. Response: '{}'"
                            "".format(resp.status, await resp.text())
                        )
        except aiohttp.ClientError as e:
            logger.debug(f"Failed to connect to server. Retrying. {e}")

        await asyncio.sleep(wait_time_between_pulls)
        attempts -= 1

    bf_nlu_banki.shared.utils.cli.print_error_and_exit(
        "Could not fetch runtime config from server at '{}'. "
        "Exiting.".format(config_endpoint)
    )


def run_in_production(args: argparse.Namespace) -> None:
    from bf_nlu_banki.shared.utils.cli import print_success

    print_success("Starting bf_nlu_banki X in production mode... 🚀")

    credentials_path, endpoints_path = _get_credentials_and_endpoints_paths(args)
    endpoints = AvailableEndpoints.read_endpoints(endpoints_path)

    _bf_nlu_banki_service(args, endpoints, None, credentials_path)


def _get_config_path(args: argparse.Namespace) -> Optional[Text]:
    config_path = bf_nlu_banki.cli.utils.get_validated_path(
        args.config, "config", DEFAULT_CONFIG_PATH
    )

    return str(config_path)


def _get_domain_path(args: argparse.Namespace) -> Optional[Text]:
    domain_path = bf_nlu_banki.cli.utils.get_validated_path(
        args.domain, "domain", DEFAULT_DOMAIN_PATH
    )

    return str(domain_path)


def _get_credentials_and_endpoints_paths(
    args: argparse.Namespace,
) -> Tuple[Optional[Text], Optional[Text]]:
    config_endpoint = args.config_endpoint
    endpoints_config_path: Optional[Union[Path, Text]]

    if config_endpoint:
        endpoints_config_path, credentials_path = asyncio.run(
            _pull_runtime_config_from_server(config_endpoint)
        )
    else:
        endpoints_config_path = bf_nlu_banki.cli.utils.get_validated_path(
            args.endpoints, "endpoints", DEFAULT_ENDPOINTS_PATH, True
        )
        credentials_path = None

    return (
        credentials_path,
        str(endpoints_config_path) if endpoints_config_path else None,
    )


def _prevent_failure_if_git_is_not_available() -> None:
    """bf_nlu_banki X uses the `git` package, which will fail to import if git is not available.

    Git isn't needed locally, which means we can silence this error to allow
    users to use local mode even if git is not available on their machine.
    Fixes regression https://github.com/bf_nlu_bankiHQ/bf_nlu_banki/issues/7140
    """
    if os.environ.get("GIT_PYTHON_REFRESH") is None:
        os.environ["GIT_PYTHON_REFRESH"] = "quiet"


def run_locally(args: argparse.Namespace) -> None:
    """Run a bf_nlu_banki X instance locally.

    Args:
        args: commandline arguments
    """
    _prevent_failure_if_git_is_not_available()

    try:
        # noinspection PyUnresolvedReferences
        from bf_nlu_bankix.community import local
    except ModuleNotFoundError:
        raise MissingDependencyException(
            f"bf_nlu_banki X does not seem to be installed, but it is needed for this "
            f"CLI command. You can find more information on how to install bf_nlu_banki X "
            f"in local mode in the documentation: "
            f"{DOCS_BASE_URL_bf_nlu_banki_X}/installation-and-setup/install/local-mode"
        )

    args.bf_nlu_banki_x_port = args.bf_nlu_banki_x_port or DEFAULT_bf_nlu_banki_X_PORT
    args.port = args.port or DEFAULT_bf_nlu_banki_PORT

    project_path = "."

    _validate_bf_nlu_banki_x_start(args, project_path)

    bf_nlu_banki_x_token = generate_bf_nlu_banki_x_token()
    process = start_bf_nlu_banki_for_local_bf_nlu_banki_x(args, bf_nlu_banki_x_token=bf_nlu_banki_x_token)

    config_path = _get_config_path(args)
    domain_path = _get_domain_path(args)

    telemetry.track_bf_nlu_banki_x_local()

    # noinspection PyBroadException
    try:
        local.main(
            args,
            project_path,
            args.data,
            token=bf_nlu_banki_x_token,
            config_path=config_path,
            domain_path=domain_path,
        )
    except bf_nlu_bankiXTermsError:
        # User didn't accept the bf_nlu_banki X terms.
        pass
    except Exception:
        print(traceback.format_exc())
        bf_nlu_banki.shared.utils.cli.print_error(
            "Sorry, something went wrong (see error above). Make sure to start "
            "bf_nlu_banki X with valid data and valid domain and config files. Please, "
            "also check any warnings that popped up.\nIf you need help fixing "
            "the issue visit our forum: https://forum.bf_nlu_banki.com/."
        )
    finally:
        process.terminate()
