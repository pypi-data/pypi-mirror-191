import random
from threading import Lock
from typing import Dict, List

import nickgen.macros_handler
from nickgen.syllable_eng import SyllableEng
from nickgen.syllable_jap import SyllableJap
from nickgen.syllable_loader import SyllableLoader


class LoginMacrossHandler:
    syllableEng_0: SyllableEng = SyllableLoader.LoadEng()
    syllableEng_1: SyllableEng = SyllableLoader.LoadLat()
    syllableJap_0: SyllableJap = SyllableLoader.LoadJap()
    syllableEng_2: SyllableEng

    macrossHandler_0 = nickgen.macros_handler.MacrossHandler("[", "]", None)
    locker = Lock()

    @classmethod
    def SetUserBase(cls, userBase: SyllableEng):
        LoginMacrossHandler.syllableEng_2 = userBase

    @classmethod
    def GetLogins(cls, macross: str, count: int) -> tuple[str]:
        if count > 0:
            with cls.locker:
                generator = (
                    cls.macrossHandler_0.ExecComplexMacross(macross)
                    for i in range(count)
                )
                return tuple(generator)
        else:
            return None

    @classmethod
    def ExecSimplMacross(cls, simplMacross: str):
        if not simplMacross:
            return ""

        strArray = simplMacross.split("|")
        str1 = strArray[0]

        try:
            if str1 == "Eng":
                return LoginMacrossHandler.syllableEng_0.GetLogins(int(strArray[1]), 1)[
                    0
                ]
            if str1 == "RndNum":
                return str(random.randint(int(strArray[1]), int(strArray[2]) - 1))
            if str1 == "RndText":
                return LoginMacrossHandler.__RndText(strArray)
            if str1 == "Jap":
                return LoginMacrossHandler.syllableJap_0.GetLogins(int(strArray[1]), 1)[
                    0
                ]
            if str1 == "Lat":
                return LoginMacrossHandler.syllableEng_1.GetLogins(int(strArray[1]), 1)[
                    0
                ]
            if str1 == "RndSym":
                return LoginMacrossHandler.__RndSym(strArray)
            if str1 == "V":
                return LoginMacrossHandler.syllableEng_0.GetChar(
                    SyllableEng.CharType.Vowel
                )
            if str1 == "C":
                return LoginMacrossHandler.syllableEng_0.GetChar(
                    SyllableEng.CharType.Consonant
                )
            if str1 == "UserDef":
                return LoginMacrossHandler.syllableEng_2.GetLogins(int(strArray[1]), 1)[
                    0
                ]

            raise Exception("Error in LoginMacrossHandler")
        except:
            pass
        return ""

    @staticmethod
    def __RndText(strArray: List[str]):
        str2 = "0123456789"
        str3 = "QWERTYUIOPASDFGHJKLZXCVBNM"
        str4 = "qwertyuiopasdfghjklzxcvbnm"
        int32_7 = int(strArray[1])
        chArray1: List[str] = []
        flag1 = False
        flag2 = False

        if len(strArray) == 3:
            if "d" in strArray[2] or "D" in strArray[2]:
                flag1 = True
            if "c" in strArray[2] or "C" in strArray[2]:
                flag2 = True

        if flag1:
            str4 += str2
        if flag2:
            str4 += str3

        length1 = len(str4)
        for i in range(int32_7):
            chArray1[i] = str4[random.randint(0, length1 - 1)]
        return "".join(chArray1)

    @staticmethod
    def __RndSym(strArray: List[str]):
        int32_8 = int(strArray[1])
        str5 = strArray[2]
        chArray2: List[str] = []
        length2 = len(str5)
        for i in range(int32_8):
            chArray2[i] = str5[random.randint(0, length2 - 1)]
        return "".join(chArray2)
