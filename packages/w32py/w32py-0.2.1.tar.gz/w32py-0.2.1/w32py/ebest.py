from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable

from loguru import logger

from w32py.win import dispatch, pumpWaitingMessages, withEvents


class CALLBACK:  # pylint: disable=too-few-public-methods
    OnDisconnect: list[Callable[[], None]] = []
    OnReceiveData: list[Callable[[dict[str, Any]], None]] = []
    OnReceiveRealData: list[Callable[[dict[str, Any]], None]] = []


class SESSION_STATUS(Enum):
    DISCONNECT = auto()
    LOGIN_SUCCEEDED = auto()
    LOGIN_FAILED = auto()


class XASessionEvents:
    def __init__(self) -> None:
        self.__debug = False
        self.__com: Any = None
        self.__status = SESSION_STATUS.DISCONNECT

    def init(self, com: Any, debug: bool = False) -> None:
        self.__debug = debug
        self.__com = com
        self.__status = SESSION_STATUS.DISCONNECT

    def OnLogin(self, szCode: str, szMsg: str) -> None:
        if self.__debug:
            logger.debug(f"{szCode}, {szMsg}")

        if szCode == "0000":
            self.__status = SESSION_STATUS.LOGIN_SUCCEEDED
            return

        logger.error(f"{szCode}, {szMsg}")
        self.__status = SESSION_STATUS.LOGIN_FAILED

    def OnLogout(self) -> None:
        logger.error("")
        self.__disconnect()
        for OnDisconnect in CALLBACK.OnDisconnect:
            OnDisconnect()

    def OnDisconnect(self) -> None:
        logger.error("")
        self.__disconnect()
        for OnDisconnect in CALLBACK.OnDisconnect:
            OnDisconnect()

    def ConnectServer(self, szServerIP: str, nServerPort: int) -> bool:
        return self.__com.ConnectServer(  # type: ignore
            szServerIP, nServerPort
        )

    def DisconnectServer(self) -> None:
        self.__com.DisconnectServer()

    def Login(  # pylint: disable=too-many-arguments
        self,
        szID: str,
        szPwd: str,
        szCertPwd: str,
        nServerType: int,
        bShowCertErrDlg: bool,
    ) -> bool:
        return self.__com.Login(  # type: ignore
            szID, szPwd, szCertPwd, nServerType, bShowCertErrDlg
        )

    def GetLastError(self) -> int:
        return self.__com.GetLastError()  # type: ignore

    def GetErrorMessage(self, nErrorCode: int) -> str:
        return self.__com.GetErrorMessage(nErrorCode)  # type: ignore

    def __disconnect(self) -> None:
        self.DisconnectServer()
        self.__status = SESSION_STATUS.DISCONNECT

    def __lastError(self, prefix: str) -> str:
        nErrCode = self.GetLastError()
        strErrMsg = self.GetErrorMessage(nErrCode)
        return f"{prefix}, {nErrCode}, {strErrMsg}"

    def login(  # pylint: disable=too-many-arguments
        self,
        szID: str,
        szPwd: str,
        szCertPwd: str,
        nServerType: int = 0,
        szServerIP: str = "hts.ebestsec.co.kr",
        nServerPort: int = 20001,
    ) -> str:
        self.__disconnect()
        if not self.ConnectServer(szServerIP, nServerPort):
            return self.__lastError("ConnectServer")
        if not self.Login(szID, szPwd, szCertPwd, nServerType, False):
            return self.__lastError("Login")

        while self.__status == SESSION_STATUS.DISCONNECT:
            pumpWaitingMessages()

        if self.__status == SESSION_STATUS.LOGIN_SUCCEEDED:
            return ""
        return "LOGIN_FAILED"


def parse_field(line: str) -> dict[str, Any]:
    cols = line.split(",")
    return {
        "name": cols[1].strip(),
        "desc": cols[0].strip(),
        "type": cols[3].strip(),
        "size": cols[4].strip(),
    }


def parse_lines(lines: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {
        "desc": "",
        "input": {},
        "output": {},
    }
    lines = list(
        filter(lambda x: x, map(lambda x: x.strip().replace(";", ""), lines))
    )
    for i, line in enumerate(lines):
        if line.startswith(".Func,") or line.startswith(".Feed,"):
            parsed["desc"] = line.split(",")[1].strip()
        elif line == "begin":
            latest_begin = i
        elif line == "end":
            block_info = lines[latest_begin - 1].split(",")
            parsed[block_info[2]][block_info[0]] = {
                "occurs": block_info[-1].startswith("occurs"),
                "fields": list(map(parse_field, lines[latest_begin + 1 : i])),
            }
    return parsed


def parse_res(p: Path) -> dict[str, Any]:
    with open(p, "rt", encoding="cp949") as fp:
        return parse_lines(fp.readlines())


class XAQueryEvents:
    def __init__(self) -> None:
        self.__debug = False
        self.__com: Any = None
        self.__meta: dict[str, Any] = {}
        self.__received = False

    def init(self, com: Any, p: Path, debug: bool = False) -> None:
        self.__debug = debug
        self.__com = com
        self.__meta = parse_res(p)
        self.__received = False
        self.PutResFileName(f"{p}")

    def OnReceiveData(self, szTrCode: str) -> None:
        block: dict[str, Any] = {}
        for szBlockName, v in self.__meta["output"].items():
            fields = v["fields"]
            if v["occurs"]:
                block[szBlockName] = [
                    self.__getBlock(szBlockName, fields, i)
                    for i in range(self.GetBlockCount(szBlockName))
                ]
            else:
                block[szBlockName] = self.__getBlock(szBlockName, fields, 0)
        responseQuery = {
            "err": "",
            "tr": szTrCode,
            "block": block,
        }
        if self.__debug:
            logger.debug(f"{responseQuery}")
        self.__received = True
        for OnReceiveData in CALLBACK.OnReceiveData:
            OnReceiveData(responseQuery)

    def OnReceiveMessage(
        self, bIsSystemError: int, nMessageCode: str, szMessage: str
    ) -> None:
        if self.__debug:
            logger.debug(f"{bIsSystemError}, {nMessageCode}, {szMessage}")

        if bIsSystemError == 0 and nMessageCode[0] == "0":
            return

        responseQuery = {
            "err": f"{bIsSystemError}, {nMessageCode}, {szMessage}",
            "tr": "",
            "block": {},
        }
        self.__received = True
        for OnReceiveData in CALLBACK.OnReceiveData:
            OnReceiveData(responseQuery)

    def GetFieldData(
        self, szBlockName: str, szFieldName: str, nRecordIndex: int
    ) -> str:
        return self.__com.GetFieldData(  # type: ignore
            szBlockName, szFieldName, nRecordIndex
        )

    def Request(self, bNext: bool) -> int:
        return self.__com.Request(bNext)  # type: ignore

    def PutResFileName(self, pVal: str) -> None:
        self.__com.ResFileName = pVal

    def SetFieldData(
        self,
        szBlockName: str,
        szFieldName: str,
        nOccursIndex: int,
        szData: str,
    ) -> None:
        self.__com.SetFieldData(szBlockName, szFieldName, nOccursIndex, szData)

    def GetBlockCount(self, szBlockName: str) -> int:
        return self.__com.GetBlockCount(szBlockName)  # type: ignore

    def GetErrorMessage(self, nErrorCode: int) -> str:
        return self.__com.GetErrorMessage(nErrorCode)  # type: ignore

    def __getBlock(
        self,
        szBlockName: str,
        fields: list[dict[str, Any]],
        nRecordIndex: int,
    ) -> dict[str, Any]:
        block: dict[str, Any] = {}
        for field in fields:
            szFieldName = field["name"]
            val = self.GetFieldData(szBlockName, szFieldName, nRecordIndex)
            block[szFieldName] = f"{val}"
        return block

    def __setBlock(
        self,
        szBlockName: str,
        fields: list[dict[str, Any]],
        nOccursIndex: int,
        block: dict[str, Any],
    ) -> str:
        for field in fields:
            szFieldName = field["name"]
            val = block.get(szFieldName)
            if val is None:
                return (
                    f"InvalidField, {szBlockName}"
                    f", {szFieldName}, {nOccursIndex}"
                )
            self.SetFieldData(szBlockName, szFieldName, nOccursIndex, f"{val}")
        return ""

    def query(  # pylint: disable=too-many-return-statements,too-many-branches
        self, requestQuery: dict[str, Any]
    ) -> str:
        if self.__debug:
            logger.debug(f"{requestQuery}")

        requestBlock = requestQuery["block"]
        for szBlockName, v in self.__meta["input"].items():
            fields = v["fields"]
            if v["occurs"]:
                blocks = requestBlock.get(szBlockName)
                if blocks is None:
                    return f"InvalidBlock, {szBlockName}"
                if not isinstance(blocks, list):
                    return (
                        f"InvalidBlockType, {szBlockName}"
                        f", list, {type(blocks)}"
                    )
                for i, block in enumerate(blocks):
                    if not isinstance(block, dict):
                        return (
                            f"InvalidBlockType, {szBlockName}"
                            f", list, {i}, dict, {type(block)}"
                        )
                    err = self.__setBlock(szBlockName, fields, i, block)
                    if err:
                        return err
            else:
                block = requestBlock.get(szBlockName)
                if block is None:
                    return f"InvalidBlock, {szBlockName}"
                if not isinstance(block, dict):
                    return (
                        f"InvalidBlockType, {szBlockName}"
                        f", dict, {type(block)}"
                    )
                err = self.__setBlock(szBlockName, fields, 0, block)
                if err:
                    return err

        nErrCode = self.Request(requestQuery["cont"])
        if nErrCode < 0:
            strErrMsg = self.GetErrorMessage(nErrCode)
            return f"Request, {nErrCode}, {strErrMsg}"

        while not self.__received:
            pumpWaitingMessages()
        return ""


class XARealEvents:
    def __init__(self) -> None:
        self.__debug = False
        self.__com: Any = None
        self.__meta: dict[str, Any] = {}
        self.__keys: set[str] = set()

    def init(self, com: Any, p: Path, debug: bool = False) -> None:
        self.__debug = debug
        self.__com = com
        self.__meta = parse_res(p)
        self.__keys = set()
        self.PutResFileName(f"{p}")

    def OnReceiveRealData(self, szTrCode: str) -> None:
        block: dict[str, Any] = {}
        for szBlockName, v in self.__meta["output"].items():
            fields = v["fields"]
            block[szBlockName] = self.__getBlock(szBlockName, fields)
        if self.__meta["input"]["InBlock"]:
            szFieldName = self.__meta["input"]["InBlock"]["fields"][0]["name"]
            key = block["OutBlock"][szFieldName]
        else:
            key = ""
        responseReal = {
            "err": "",
            "tr": szTrCode,
            "key": key,
            "block": block,
        }
        if self.__debug:
            logger.debug(f"{responseReal}")
        for OnReceiveRealData in CALLBACK.OnReceiveRealData:
            OnReceiveRealData(responseReal)

    def PutResFileName(self, pVal: str) -> None:
        self.__com.ResFileName = pVal

    def SetFieldData(
        self, szBlockName: str, szFieldName: str, szData: str
    ) -> None:
        self.__com.SetFieldData(szBlockName, szFieldName, szData)

    def GetFieldData(self, szBlockName: str, szFieldName: str) -> str:
        return self.__com.GetFieldData(  # type: ignore
            szBlockName, szFieldName
        )

    def AdviseRealData(self) -> None:
        self.__com.AdviseRealData()

    def UnadviseRealData(self) -> None:
        self.__com.UnadviseRealData()

    def UnadviseRealDataWithKey(self, szCode: str) -> None:
        self.__com.UnadviseRealDataWithKey(szCode)

    def __getBlock(
        self,
        szBlockName: str,
        fields: list[dict[str, Any]],
    ) -> dict[str, Any]:
        block: dict[str, Any] = {}
        for field in fields:
            szFieldName = field["name"]
            val = self.GetFieldData(szBlockName, szFieldName)
            block[szFieldName] = f"{val}"
        return block

    def advise(self, requestReal: dict[str, Any]) -> str:
        if self.__debug:
            logger.debug(f"{requestReal}")

        key = requestReal["key"]
        if key in self.__keys:
            return ""

        if key:
            self.SetFieldData(
                "InBlock",
                self.__meta["input"]["InBlock"]["fields"][0]["name"],
                key,
            )
        self.AdviseRealData()
        self.__keys.add(key)
        return ""

    def unadvise(self, requestReal: dict[str, Any]) -> str:
        if self.__debug:
            logger.debug(f"{requestReal}")

        key = requestReal["key"]
        if key not in self.__keys:
            return ""

        if key:
            self.UnadviseRealDataWithKey(key)
        else:
            self.UnadviseRealData()
        self.__keys.remove(key)
        return ""


class Meta:
    def __init__(
        self, path: str = "C:/eBEST/xingAPI/Res", debug: bool = False
    ) -> None:
        self.__debug = debug
        self.__path = Path(path)
        com = dispatch("XA_Session.XASession")
        obj = withEvents(com, XASessionEvents)
        obj.init(com, debug=self.__debug)
        self.__XASession = obj
        self.__XAQueryDict: dict[str, Any] = {}
        self.__XARealDict: dict[str, Any] = {}

    def __enter__(self) -> Any:
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.__XASession.DisconnectServer()

    def exists(self, szTrCode: str) -> tuple[bool, Path]:
        p = self.__path / f"{szTrCode}.res"
        return p.exists(), p

    def getXASession(self) -> Any:
        return self.__XASession

    def getXAQuery(self, szTrCode: str) -> Any:
        obj = self.__XAQueryDict.get(szTrCode)
        if obj is None:
            b, p = self.exists(szTrCode)
            if not b:
                return None
            com = dispatch("XA_DataSet.XAQuery")
            obj = withEvents(com, XAQueryEvents)
            obj.init(com, p, debug=self.__debug)
            self.__XAQueryDict[szTrCode] = obj
        return obj

    def getXAReal(self, szTrCode: str) -> Any:
        obj = self.__XARealDict.get(szTrCode)
        if obj is None:
            b, p = self.exists(szTrCode)
            if not b:
                return None
            com = dispatch("XA_DataSet.XAReal")
            obj = withEvents(com, XARealEvents)
            obj.init(com, p, debug=self.__debug)
            self.__XARealDict[szTrCode] = obj
        return obj

    def login(  # pylint: disable=too-many-arguments
        self,
        szID: str,
        szPwd: str,
        szCertPwd: str,
        nServerType: int = 0,
        szServerIP: str = "hts.ebestsec.co.kr",
        nServerPort: int = 20001,
    ) -> str:
        obj = self.getXASession()
        return obj.login(  # type: ignore
            szID,
            szPwd,
            szCertPwd,
            nServerType=nServerType,
            szServerIP=szServerIP,
            nServerPort=nServerPort,
        )

    def query(self, requestQuery: dict[str, Any]) -> str:
        tr = requestQuery["tr"]
        obj = self.getXAQuery(tr)
        if obj is None:
            return f"FileNotFound, {tr}.res"
        return obj.query(requestQuery)  # type: ignore

    def advise(self, requestReal: dict[str, Any]) -> str:
        tr = requestReal["tr"]
        obj = self.getXAReal(tr)
        if obj is None:
            return f"FileNotFound, {tr}.res"
        return obj.advise(requestReal)  # type: ignore

    def unadvise(self, requestReal: dict[str, Any]) -> str:
        tr = requestReal["tr"]
        obj = self.getXAReal(tr)
        if obj is None:
            return f"FileNotFound, {tr}.res"
        return obj.unadvise(requestReal)  # type: ignore
