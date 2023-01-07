import os
import sys
import platform

from src.utils.printing import freeze_panic
from src.client import *


def check_user() -> None:
    if os.getuid() == 0:
        freeze_panic("Please do not run freeze as root! It may be dangerous!", True)
        sys.exit(1)


def check_platform() -> None:
    if platform.system() == 'windows':
        freeze_panic("This program was made for linux only!", True)
        sys.exit(1)


def check_args() -> None:
    if len(sys.argv) == 1:
        freeze_panic("you must specify a command!", True)
        sys.exit(1)

    if sys.argv[1].lower() not in accepted_args:
        freeze_panic(f"invalid command: {sys.argv[1]}", True)
        sys.exit(1)

    if sys.argv[1] == 'install' and len(sys.argv) <= 2:
        freeze_panic("you must specify at least one package name!", True)
        sys.exit(1)

    if sys.argv[1] == 'remove' and len(sys.argv) <= 2:
        freeze_panic("you must specify at least one package name!", True)
        sys.exit(1)

    if sys.argv[1] == 'search':
        if len(sys.argv) <= 2:
            freeze_panic("you must specify a package name!", True)
            sys.exit(1)

        if len(sys.argv) >= 4:
            freeze_panic("You can only search for one package at a time!", True)
            sys.exit(1)

    if sys.argv[1] == 'help' and len(sys.argv) >= 3:
        freeze_panic("Help only takes one argument!", True)
        sys.exit(1)

    if sys.argv[1] == 'update' and len(sys.argv) >= 3:
        freeze_panic("Update only takes one argument!", True)
        sys.exit(1)

    if sys.argv[1] == 'version' and len(sys.argv) >= 3:
        freeze_panic("version only takes one argument!", True)
        sys.exit(1)


def run_checks() -> None:
    check_user()
    check_platform()
    check_args()


def main() -> None:
    run_checks()

    args_orig: list = sys.argv
    args: list = rebuild_args(args_orig)

    match args_orig[1]:
        case 'install':
            download(args)
        case 'search':
            pkg: str = args[0]
            search(pkg)
        case 'remove':
            remove(args)
        case 'version':
            version()
        case 'help':
            freeze_help()


if __name__ == '__main__':
    main()
