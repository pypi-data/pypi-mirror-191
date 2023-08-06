from sys import argv
from typing import Any

from psutil import process_iter
from PyQt5.QAxContainer import QAxWidget  # pylint: disable=no-name-in-module
from PyQt5.QtCore import QEventLoop  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
from pythoncom import (  # pylint: disable=no-name-in-module
    CoInitialize,
    CoUninitialize,
    PumpWaitingMessages,
)
from pywinauto import Application
from win32com.client import Dispatch, WithEvents


def coInitialize() -> None:
    CoInitialize()


def coUninitialize() -> None:
    CoUninitialize()


class COM:
    def __enter__(self) -> Any:
        coInitialize()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        coUninitialize()


def pumpWaitingMessages() -> int:
    """
    Returns 1 if a WM_QUIT message was received, else 0
    """
    return PumpWaitingMessages()  # type: ignore


def dispatch(clsid: Any) -> Any:
    return Dispatch(clsid)


def withEvents(obj: Any, user_event_class: Any) -> Any:
    return WithEvents(obj, user_event_class)


def startApplication(cmd: str, backend: str = "win32") -> Application:
    return Application(backend=backend).start(cmd)


def isRunning(names: set[str]) -> bool:
    for proc in process_iter():
        if proc.name() in names:
            return True
    return False


def qAxWidget(control: str) -> QAxWidget:
    return QAxWidget(control)


def qApplication() -> QApplication:
    return QApplication(argv)


def qEventLoop() -> QEventLoop:
    return QEventLoop()
