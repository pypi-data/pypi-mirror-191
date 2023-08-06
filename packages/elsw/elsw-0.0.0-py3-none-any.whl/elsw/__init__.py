#!/usr/bin/env python3


"""
A nice way to view Portage world file.
""" """

This file is part of elsw - a nice way view Portage world file.
Copyright (c) 2019-2023, Maciej Barć <xgqt@riseup.net>
Licensed under the GNU GPL v2 License
SPDX-License-Identifier: GPL-2.0-or-later

elsw is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

elsw is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with elsw.  If not, see <https://www.gnu.org/licenses/>.
"""


import argparse

import colorama


try:
    import portage

    if portage.root is None:
        portage.root = "/"

    WORLD_FILE = portage.root + portage.WORLD_FILE
    WORLD_SETS_FILE = portage.root + "var/lib/portage/world_sets"
    PORTAGE_SETS_DIR = portage.root + "etc/portage/sets/"

except ImportError:
    print("WARNING: Could not import portage")

    WORLD_FILE = "/var/lib/portage/world"
    WORLD_SETS_FILE = "/var/lib/portage/world_sets"
    PORTAGE_SETS_DIR = "/etc/portage/sets/"


__description__ = "View the Portage world file"
__version__ = "0.0.0"


def read_content(file_path):
    """
    Read contents of a file removing comment lines.
    """

    contents = []

    with open(file_path, mode="r", encoding="utf-8") as opened_file:
        while True:
            file_line = opened_file.readline()
            if not file_line:
                break

            stripped_line = file_line.strip()
            if len(stripped_line) != 0 or stripped_line[0] != "#":
                contents.append(stripped_line)

    return contents


def get_sets_pkgs(with_world: bool):
    """
    Get packages in the @system set and in installed sets.
    """

    pkgs = read_content(WORLD_FILE) if with_world else []

    for portage_set in read_content(WORLD_SETS_FILE):
        for line in read_content(PORTAGE_SETS_DIR + portage_set):
            pkgs.append(f"{line} \033[0m@{portage_set}")

    return pkgs


def choose_color(category):
    """
    Colorize.
    """

    color_good = colorama.Fore.GREEN
    color_warn = colorama.Fore.YELLOW
    color_erro = colorama.Fore.RED

    category_warn = [
        "app-crypt", "app-dicts", "app-emacs", "app-i18n",
        "dev-cpp", "dev-lang", "dev-perl", "dev-texlive",
        "gui-wm",
        "media-plugins",
        "net-dns", "net-p2p",
        "sci-libs",
        "sys-apps", "sys-auth", "sys-firmware", "sys-fs", "sys-libs",
        "x11-apps", "x11-base", "x11-misc", "x11-plugins"
    ]
    category_erro = [
        "acct-group", "acct-user",
        "dev-libs",
        "gnustep-libs", "gui-libs",
        "java-virtuals",
        "media-libs",
        "net-libs",
        "sci-libs", "sec-policy", "sys-libs",
        "virtual",
        "x11-drivers", "x11-libs", "x11-wm"
    ]

    if category in category_warn:
        return color_warn
    if category in category_erro:
        return color_erro
    return color_good


def parse_category(category):
    """
    Parse categories
    Add special characters
    """

    return f"{4 * ' '}{choose_color(category)} \u25cf {category}"


def main():
    """
    Main.
    """

    parser = argparse.ArgumentParser(
        description=f"%(prog)s - {__description__}",
        epilog="""Copyright (c) 2019-2023, Maciej Barć <xgqt@riseup.net>
    Licensed under the GNU GPL v2 License"""
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="List all available packages"
    )
    parser.add_argument(
        "-i", "--installed",
        action="store_true",
        help="List @installed packages"
    )
    parser.add_argument(
        "-w", "--world",
        action="store_true",
        help="List @world set(s) packages"
    )
    parser.add_argument(
        "-s", "--sets",
        action="store_true",
        help="List non-@world packages"
    )
    parser.add_argument(
        "-e", "--exclude",
        type=str,
        default="",
        help="""Exclude package categories from being listed
    (pass in a delimited list string)"""
    )
    args = parser.parse_args()

    if args.all:
        extracted_packages = portage.db[portage.root]["porttree"].getallnodes()
    elif args.installed:
        extracted_packages = portage.db[portage.root]["vartree"].getallnodes()
    elif args.sets:
        extracted_packages = get_sets_pkgs(False)
    else:
        extracted_packages = get_sets_pkgs(True)

    colorama.init(autoreset=True, strip=False)

    category_tmp = ""
    group_tmp = ""
    category_count = 0
    package_count = 0
    category_package_count = 0

    for pkg in sorted(list(set(extracted_packages))):
        read_category = pkg.split("/")[0]
        read_group = read_category.split("-")[0]
        read_name = pkg.split("/")[1]

        if args.exclude != "" and read_category in args.exclude.split(","):
            continue

        # Print LAST category count result
        if read_category != category_tmp and category_package_count != 0:
            print(f"{colorama.Fore.WHITE}{6 * ' '} = {category_package_count}")

        if read_group != group_tmp:
            print(f"{colorama.Fore.WHITE} \u25cb {str.upper(read_group)}")
            group_tmp = read_group

        if read_category != category_tmp:
            # Print new category header
            print(parse_category(read_category))
            category_tmp = read_category
            category_count += 1
            category_package_count = 0

        print(f"{colorama.Fore.BLUE}{8 * ' '} - {read_name}")
        package_count += 1
        category_package_count += 1

    # Final category count
    print(f"{colorama.Fore.WHITE}{6 * ' '} = {category_package_count}")

    # Reset color + newline
    print("\033[0m")

    print(f"{category_count} categories")
    print(f"{package_count} packages")


if __name__ == "__main__":
    main()
