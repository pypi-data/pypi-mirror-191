import sys
from typing import Any, Text, NoReturn

import bf_nlu_banki.shared.utils.io


def print_color(*args: Any, color: Text) -> None:
    output = bf_nlu_banki.shared.utils.io.wrap_with_color(*args, color=color)
    try:
        # colorama is used to fix a regression where colors can not be printed on
        # windows. https://github.com/bf_nlu_bankiHQ/bf_nlu_banki/issues/7053
        from colorama import AnsiToWin32

        stream = AnsiToWin32(sys.stdout).stream
        print(output, file=stream)
    except ImportError:
        print(output)


def print_success(*args: Any) -> None:
    print_color(*args, color=bf_nlu_banki.shared.utils.io.bcolors.OKGREEN)


def print_info(*args: Any) -> None:
    print_color(*args, color=bf_nlu_banki.shared.utils.io.bcolors.OKBLUE)


def print_warning(*args: Any) -> None:
    print_color(*args, color=bf_nlu_banki.shared.utils.io.bcolors.WARNING)


def print_error(*args: Any) -> None:
    print_color(*args, color=bf_nlu_banki.shared.utils.io.bcolors.FAIL)


def print_error_and_exit(message: Text, exit_code: int = 1) -> NoReturn:
    """Print error message and exit the application."""

    print_error(message)
    sys.exit(exit_code)
