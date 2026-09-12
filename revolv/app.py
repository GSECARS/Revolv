# SPDX-License-Identifier: MIT

import os
import sys
from contextlib import suppress
from importlib.metadata import version
from importlib.resources import as_file, files

import wx

from revolv.controller import MainController
from revolv.view import MainView

__all__ = ["RevolvApp", "start_ui"]


class RevolvApp(wx.App):
    """Manage the wx application lifecycle."""

    def __init__(self, *args, **kwargs) -> None:
        self._set_dpi_awareness()
        super().__init__(*args, **kwargs)

    def OnInit(self) -> bool:
        """Configures thre application during wx initialization."""
        self._configure_app(name="Revolv")
        self._set_macos_dock_icon()
        return True

    def run(self, window: wx.Frame) -> None:
        """Display the main window and start the event loop."""
        self.SetTopWindow(window)
        window.Show()
        wx.CallAfter(self._activate_window, window)
        self.MainLoop()

    def _configure_app(self, name: str) -> None:
        self.SetAppDisplayName(name)

        if sys.platform == "darwin":
            with suppress(Exception):
                from Foundation import NSBundle

                info = NSBundle.mainBundle().infoDictionary()
                if info is not None:
                    info["CFBundleName"] = name

    @staticmethod
    def _activate_window(window: wx.Frame) -> None:
        """Activate an raise the main window."""
        if sys.platform == "darwin":
            with suppress(Exception):
                from AppKit import NSApplication

                NSApplication.sharedApplication().activateIgnoringOtherApps_(True)

        window.Raise()

    @staticmethod
    def _set_dpi_awareness() -> None:
        if sys.platform == "win32":
            try:
                wx.App.SetDPIAwareness(wx.DPI_AWARENESS_CTX_PER_MONITOR_AWARE_V2)
            except AttributeError:
                import ctypes

                ctypes.windll.shcore.SetProcessDpiAwareness(2)

    @staticmethod
    def _set_macos_dock_icon() -> None:
        if sys.platform != "darwin":
            return

        with suppress(Exception):
            from AppKit import NSApplication, NSImage, NSData

            icon_bytes = files("revolv").joinpath("assets", "revolv.icns").read_bytes()
            data = NSData.dataWithBytes_length_(icon_bytes, len(icon_bytes))
            image = NSImage.alloc().initWithData_(data)

            NSApplication.sharedApplication().setApplicationIconImage_(image)


def create_shortcut(public: bool = False, folder: str | None = None) -> None:
    """Create a platform-native shortcut."""
    from pyshortcuts import make_shortcut

    extension = {"darwin": "icns", "win32": "ico"}.get(sys.platform, "png")
    resource = files("revolv").joinpath("assets", f"revolv.{extension}")

    with as_file(resource) as icon:
        kws = dict(name="Revolv", description=f"Revolv {version('revolv')}", icon=str(icon), terminal=False, public=public, folder=folder)

        if sys.platform == "darwin":
            kws["macos_app"] = True

        bindir = "Scripts" if os.name == "nt" else "bin"
        script = os.path.join(sys.prefix, bindir, "revolv")
        make_shortcut(script, **kws)


def start_ui() -> None:
    """Construct and start the Revolv GUI."""
    app = RevolvApp(False)
    view = MainView(version=version("revolv"))
    MainController(view=view)

    app.run(view)
