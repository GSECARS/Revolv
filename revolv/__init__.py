import argparse


def main() -> None:
    """Main entry point for `revolv` console script."""
    parser = argparse.ArgumentParser("Revolv CLI")
    parser.add_argument("-m", "--make-icon", action="store_true", help="create desktop shortcut icon")
    parser.add_argument("-g", "--gui", action="store_true", help="launch the GUI application")

    args = parser.parse_args()

    if args.make_icon:
        pass
    elif args.gui:
        pass
    else:
        parser.print_help()
