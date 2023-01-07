import os
import sys
import json
import requests
from requests import HTTPError

from src.utils.printing import *

accepted_args: list[str] = ["install", "update", "search", "remove", "version", "help"]


def rebuild_args(args: list) -> list:
    args_rebuilt = []
    for i in range(2, len(args)):
        args_rebuilt.append(args[i])

    return args_rebuilt


def package_list(args) -> str:
    package_string: str = ''
    for i in range(0, len(args)):
        package_string += f" {args[i]}"

    return package_string


def download(args: list) -> None:
    freeze_panic("This command is very likely broken... Use at your own risk.\n", True)

    freeze_info(f"Following {len(args)} package(s) will be installed,{package_list(args)}", True)
    ans: str = input(freeze_question("Continue?"))

    if ans.lower() == 'y':
        for i in range(0, len(args)):
            freeze_info(f"Downloading {args[i]}", True)

            install_str: str = f"https://aur.archlinux.org/{args[i]}.git"

            os.system(f"git clone {install_str}")
            os.chdir(args[i])
            os.system(f"makepkg -si")
            os.chdir("..")

            rm_folder: str = input(freeze_question("Remove folder git folder?"))
            if rm_folder.lower() == 'y':
                os.system(f"rm -rf {args[i]}")
    else:
        freeze_info(f"Okay, goodbye!", True)
        sys.exit(0)


def search(pkg: str) -> None:
    req = requests.get(f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={pkg}")
    try:
        req.raise_for_status()

        data = req.json()

        if not data["results"]:
            freeze_info(f"Results for {pkg} not found", True)
            sys.exit(0)

        if data["resultcount"] <= 40:
            print(f'{data["resultcount"]} results found.\n')
        else:
            print(f'{data["resultcount"]} results found, but only showing 40.\n')

        for i in range(0, len(data["results"])):
            is_dated: bool = False
            if data["results"][i]["OutOfDate"]:
                is_dated = True

            print(freeze_aur(data["results"][i]["Name"], data["results"][i]["ID"], is_dated))
            print(f'    {data["results"][i]["Description"]}\n')
            if i > 40:
                break
    except HTTPError:
        freeze_panic("Something went terribly wrong!", True)


def remove(pkgs: list):
    pkg_str: str = package_list(pkgs)

    freeze_info(f"Following {len(pkgs)} package(s) will be removed,{pkg_str}", True)
    ans: str = input(freeze_question("Continue?"))

    if ans.lower() == 'y':
        if os.path.exists("/usr/bin/sudo"):
            os.system(f"sudo pacman -Rns{pkg_str}")
        elif os.path.exists("/usr/bin/doas"):
            os.system(f"doas pacman -Rns{pkg_str}")
        else:
            os.system(f"su -c pacman -Rns{pkg_str}")

        freeze_info("Done, thank you for your time!", True)
    else:
        freeze_info(f"Okay, goodbye!", True)
        sys.exit(0)


def version():
    version_str: str = "freeze 0.3 early beta, release 1"
    print(version_str)


def freeze_help():
    help_str: str = r'''Usage: freeze [options] [package]
    
Freeze, the shivering (and very simple) AUR helper.
    
Options:
    help:       Show this help message.
    version:    Show the current installed version of freeze.
    
AUR Options:
    install:    Download one or more packages from the AUR.
    update:     Update packages.
    search:     Search for packages in the AUR.
    remove:     Remove one or more packages.
'''

    print(help_str)
