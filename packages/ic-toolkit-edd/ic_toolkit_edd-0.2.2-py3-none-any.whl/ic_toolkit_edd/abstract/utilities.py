import os
import platform
import tkinter as tk
from enum import Enum


def read_credentials():
    if os.path.exists(credentials_path()):
        credentials_file = open(f"{credentials_path()}/.credentials", "r")
        credentials = credentials_file.read().split("\n")
        user_db = credentials[0].replace("userDB:", "")
        password_db = credentials[1].replace("passwordDB:", "")
        host_db = credentials[2].replace("hostDB:", "")
        port_db = credentials[3].replace("portDB:", "")
        name_db = credentials[4].replace("nameDB:", "")
        user_ic = credentials[5].replace("userIC:", "")
    else:
        return

    return {
        "userDB": user_db,
        "passwordDB": password_db,
        "hostDB": host_db,
        "portDB": port_db,
        "nameDB": name_db,
        "userIC": user_ic
    }


def credentials_path():
    if platform.system() == "Windows":
        return f"C:/Users/{os.getlogin()}/.intuitivecare"
    else:
        return f"{os.path.expanduser('~')}/.intuitivecare"


class Clipboard:
    def __init__(self):
        self._tk = tk.Tk()
        self._tk.withdraw()

    def copy(self, text: str) -> None:
        self._tk.clipboard_clear()
        self._tk.clipboard_append(text)
        self._tk.after(500, self._tk.destroy)
        self._tk.mainloop()

    def paste(self) -> str:
        try:
            return self._tk.clipboard_get()
        except Exception as e:
            return ""


class FileIdTypes(str, Enum):
    original = "original"
    parseado = "parseado"
    padronizado = "padronizado"
    arquivo = "arquivo"


class FileExtensions(str, Enum):
    csv = "csv"
    html = "html"
    json = "json"
    pdf = "pdf"
    txt = "txt"
    xls = "xls"
    xlsm = "xlsm"
    xlsx = "xlsx"
    xml = "xml"
    zip = "zip"


class PdfStrippers(str, Enum):
    raw = "raw",
    layout = "layout",
    ordered_raw = "ordered_raw",
    ordered_layout = "ordered_layout"


class PipelineSteps(str, Enum):
    parsing = "pars",
    padronizacao = "padr",
    load = "load",
    pos_proc = "proc"

    @classmethod
    def required_id(cls, step: "PipelineSteps") -> FileIdTypes:
        if step == cls.parsing:
            return FileIdTypes.original
        if step == cls.padronizacao:
            return FileIdTypes.parseado
        if step == cls.load:
            return FileIdTypes.padronizado
        if step == cls.pos_proc:
            return FileIdTypes.arquivo
