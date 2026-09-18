# SPDX-License-Identifier: MIT

from argparse import ArgumentParser
from importlib.metadata import version
from pathlib import Path

from wxutils import AppConfig, WxApplication, add_shortcut_arguments, handle_shortcut_arguments

from revolv.controller.main_controller import MainController
from revolv.view import MainView

__version__ = version("revolv")
__all__ = ["__version__", "main"]

APP_CONFIG = AppConfig(
    name="Revolv",
    assets=str(Path(__file__).resolve().parent / "assets"),
    description="X-ray scanning and data collection application",
    application_id="gsecars.revolv",
)


def make_parser():
    """Build the revolv command line parser."""
    parser = ArgumentParser("revolv")
    add_shortcut_arguments(parser)
    return parser


def start_ui():
    """Construct and start the GUI."""
    app = WxApplication(APP_CONFIG, False)
    view = MainView(version=__version__)
    _controller = MainController(view=view)

    app.run(view)


def main() -> None:
    """Main revolv entry point."""
    parser = make_parser()
    args = parser.parse_args()

    if handle_shortcut_arguments(parser, args, APP_CONFIG):
        return

    start_ui()
