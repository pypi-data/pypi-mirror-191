from sapmanager.exceptions import SapLoginError, SapConnectionError
from win32com.client import CDispatch, GetObject
from win32gui import FindWindowEx
from subprocess import Popen
from typing import Union
import os


class Sap(object):
    """Starts SAP logged into the selected system with the credentials provided, facilitating Scripting.

    Attributes
    ----------
    - system(`str`): the system you will use
    - mandt(`str`): the mandt you will use in the system
    - user(`str`): the user of the account you will use to login
    - password(`str`): the password of the account you will use to login
    - path(`str`): the path to saplogon.exe, If `None` the path used in the default SAP installation will be used
    - language(`str`) the language that will be used in SAP, by default is "EN"
    """

    def __new__(cls, system: str, mandt: str, user: str, password: str, path: str = None, language="EN") -> Union[CDispatch, None]:
        system = cls.__check_str_arg(system, "system")
        mandt = cls.__check_str_arg(mandt, "mandt")
        user = cls.__check_str_arg(user, "user")
        password = cls.__check_str_arg(password, "password")
        language = cls.__check_str_arg(language, "language")
        path = cls.__check_path(path)

        Popen(path, shell=True)
        while True:
            if FindWindowEx(None, None, None, "SAP Logon 740") != 0:
                break
        SapGuiAuto = GetObject('SAPGUI')
        if not type(SapGuiAuto) == CDispatch:
            return

        application = SapGuiAuto.GetScriptingEngine
        if not type(application) == CDispatch:
            SapGuiAuto = None
            return
        try:
            connection = application.OpenConnection(system)
        except Exception:
            raise SapConnectionError(f'Could not open connection to System "{system}"')

        if not type(connection) == CDispatch:
            application = None
            SapGuiAuto = None
            return

        session = connection.Children(0)
        if not type(session) == CDispatch:
            connection = None
            application = None
            SapGuiAuto = None
            return

        session.findById("wnd[0]/usr/txtRSYST-MANDT").text = mandt
        session.findById("wnd[0]/usr/txtRSYST-BNAME").text = user
        session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = password
        session.findById("wnd[0]/usr/txtRSYST-LANGU").text = language
        session.findById("wnd[0]").sendVKey(0)

        if session.Info.user:
            if session.ActiveWindow.Text == "Copyright":
                session.findById("wnd[1]").sendVKey(0)
            return session
        else:
            error = session.findById("wnd[0]/sbar").text
            raise SapLoginError(error)

    @classmethod
    def __check_str_arg(cls, arg, arg_name):
        if not isinstance(arg, str):
            raise ValueError(f"{arg_name} must be str")
        return arg

    @classmethod
    def __check_path(cls, path):
        if path is None:
            if os.path.exists(r"C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe"):
                return r"C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe"
            else:
                OSError("saplogon.exe not found")
        if not isinstance(path, str):
            raise ValueError("the path must be str")
        if not os.path.exists(path):
            raise OSError("saplogon.exe not found")
        return path
