# SPDX-License-Identifier: MIT

from argparse import ArgumentParser
from importlib.metadata import version

__version__ = version("revolv")
__all__ = ["__version__", "main"]


def main() -> None:
    """Main revolv entry point."""
    parser = ArgumentParser()
    parser.add_argument("-m", "--make-icon", action="store_true", help="creates a desktop/application shortcut")
    parser.add_argument("-p", "--public", dest="public_folder", nargs="?", const="GSE Apps", metavar="FOLDER", help="creates a public shortcut")
    args = parser.parse_args()

    if args.make_icon:
        from revolv.app import create_shortcut

        create_shortcut(public=args.public_folder is not None, folder=args.public_folder)
        return

    from revolv.app import start_ui

    start_ui()
