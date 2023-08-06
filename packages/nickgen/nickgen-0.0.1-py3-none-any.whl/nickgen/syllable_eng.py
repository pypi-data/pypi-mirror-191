from importlib.abc import PathEntryFinder
import re
import random
from typing import Pattern, Dict, List

from random import Random
from enum import Enum
from collections import OrderedDict

from nickgen.syllable_chain import SyllableChain
from nickgen.ForSyllableGroups import ForSyllableGroups
from nickgen.syllable_groups import SyllableGroups

class SyllableEng:

    CharType = Enum('CharType', 'Vowel Consonant')

    IsReady :bool #get; set;

    def __init__(self):
        self.string_0 :str = "VoidSyllable"
        self.string_1 :str = "VoidGroup"
        self.DwvbpfyYn :str = "ccgc"
        self.string_2 :str = "cgcc"
        self.string_3 :str = "cgc"
        self.string_4 :str = "cgg"
        self.string_5 :str = "cg"
        self.string_6 :str = "gc"

        self.dictionary_0 :Dict[str, SyllableChain] = dict()
        self.syllableGroups_0 :SyllableGroups = SyllableGroups()
        self.sortedList_0 = list()

        #self.random_0 = random
        self.regex_0 :Pattern = re.compile(r'[bcdfjghklmnpqrstvwxz01234][bcdfjghklmnpqrstvwxz01234][aeiouy56789][bcdfjghklmnpqrstvwxz01234]')
        self.regex_1 :Pattern = re.compile(r'[bcdfjghklmnpqrstvwxz01234][aeiouy56789][bcdfjghklmnpqrstvwxz01234][bcdfjghklmnpqrstvwxz01234](?=[bcdfjghklmnpqrstvwxz01234\\#])')
        self.regex_2 :Pattern = re.compile(r'[bcdfjghklmnpqrstvwxz01234][aeiouy56789][bcdfjghklmnpqrstvwxz01234](?=[bcdfjghklmnpqrstvwxz01234\\#])')
        self.regex_3 :Pattern = re.compile(r'[bcdfjghklmnpqrstvwxz01234][aeiouy56789][aeiouy56789]')
        self.regex_4 :Pattern = re.compile(r'[bcdfjghklmnpqrstvwxz01234][aeiouy56789](?=[bcdfjghklmnpqrstvwxz01234\\#])')
        self.regex_5 :Pattern = re.compile(r'[aeiouy56789][bcdfjghklmnpqrstvwxz01234]')
        self.regex_6 :Pattern = re.compile(r'[a-zA-Z]+')

    def AddTextEn(self, text:str):
        text = text.lower()
        matchCollection = self.regex_6.findall(text)
        if len(matchCollection) == 0:
            return
        
        for capture in matchCollection:
            self.AddWordEn(capture)
        
    def method_1(self, char_0: str):
        #refactor this to constant dict
        table :Dict[str,bool] = {
            '0':False,
            '1':False,
            '2':False,
            '3':False,
            '4':False,
            '5':True,
            '6':True,
            '7':True,
            '8':True,
            '9':True,
            'a':True,
            'b':False,
            'c':False,
            'd':False,
            'e':True,
            'f':False,
            'g':False,
            'h':False,
            'i':True,
            'j':False,
            'k':False,
            'l':True,
            'm':False,
            'n':False,
            'o':True,
            'p':False,
            'q':False,
            'r':False,
            's':False,
            't':False,
            'u':True,
            'v':False,
            'w':False,
            'x':False,
            'y':True,
            'z':False,
        }

        return table[char_0]

    def GetChar(self, charType: CharType):
        # Vowel, Consonant => Гласный, Согласный
        str__ = ''

        if charType is not charType.Vowel:
            str__ = 'bcdfghjklmnpqrstvwxz'
        else:
            str__ = 'aeouyi'

        length = len(str__)
        randValue = random.randint(0, length - 1)
        return str__[randValue]
    
    def AddWordEn(self, word: str):
        # if word in self.sortedList_0:
        #     return

        for tup in self.sortedList_0:
            if word == tup[0]:
                return
        
        self.sortedList_0.append((word,False))
        self.sortedList_0 = sorted(self.sortedList_0, key=lambda x: x[0])
        stringList1 = []
        stringList2 = []
        flag :bool = False

        word = self.method_3(word)
        word += '#'
        if not word:
            return
        
        while (flag is False and word):
            match1 = self.regex_0.search(word)
            if (match1 and match1.pos == 0):
                mValue1 = match1.group(0)
                stringList1.append(mValue1)
                stringList2.append('ccgc')
                word = word[len(mValue1):(len(word) - len(mValue1))]
            else:
                match2 = self.regex_1.search(word)
                if (match2 and match2.pos == 0):
                    mValue2 = match2.group(0)
                    stringList1.append(mValue2)
                    stringList2.append('cgcc')
                    word = word[len(mValue2):(len(word) - len(mValue2))]
                else:
                    match3 = self.regex_2.search(word)
                    if (match3 and match3.pos == 0):
                        mValue3 = match3.group(0)
                        stringList1.append(mValue3)
                        stringList2.append('cgc')
                        word = word[len(mValue3):(len(word) - len(mValue3))]
                    else:
                        match4 = self.regex_3.search(word)
                        if (match4 and match4.pos == 0):
                            mValue4 = match4.group(0)
                            stringList1.append(mValue4)
                            stringList2.append('cgg')
                            word = word[len(mValue4):(len(word) - len(mValue4))]
                        else:
                            match5 = self.regex_4.search(word)
                            if (match5 and match5.pos == 0):
                                mValue5 = match5.group(0)
                                stringList1.append(mValue5)
                                stringList2.append('cg')
                                word = word[len(mValue5):(len(word) - len(mValue5))]
                            else:
                                match6 = self.regex_5.search(word)
                                if (match6 and match6.pos == 0):
                                    mValue6 = match6.group(0)
                                    stringList1.append(mValue6)
                                    stringList2.append('gc')
                                    word = word[len(mValue6):(len(word) - len(mValue6))]
                                else:
                                    flag = True

        for i, item in enumerate(stringList1):
            stringList1[i] = self.method_4(item)

        stringList1.append('VoidSyllable')
        stringList1.append('VoidGroup')

        for i, item in enumerate(stringList1[:-1]):
            if item in self.dictionary_0:
                self.dictionary_0[item].AddForwardSyllable(stringList1[i + 1])
            else:
                syllableChain :SyllableChain = SyllableChain(item)
                self.dictionary_0[syllableChain.Name] = syllableChain
                syllableChain.AddForwardSyllable(stringList1[i + 1])

        for i, item in enumerate(stringList2[:-1]):
            self.syllableGroups_0.AddSyllableInGroup(item, stringList1[i])
            self.syllableGroups_0.AddForwardGroup(item, stringList2[i + 1])

        pass

    def method_2(self, string_7: str):
        matches = self.regex_6.findall(string_7)
        return ''.join(matches)
    
    def method_3(self, string_7: str):
        string_7 = string_7.replace('ch', '0')
        string_7 = string_7.replace('ph', '1')
        string_7 = string_7.replace('th', '2')
        string_7 = string_7.replace('zh', '3')
        string_7 = string_7.replace('wh', '4')
        string_7 = string_7.replace('sh', '@')
        string_7 = string_7.replace('ee', '5')
        string_7 = string_7.replace('ea', '6')
        string_7 = string_7.replace('oo', '7')
        string_7 = string_7.replace('ua', '8')
        string_7 = string_7.replace('ou', '9')
        return string_7

    def method_4(self, string_7: str):
        string_7 = string_7.replace("0", "ch")
        string_7 = string_7.replace("1", "ph")
        string_7 = string_7.replace("2", "th")
        string_7 = string_7.replace("3", "zh")
        string_7 = string_7.replace("4", "wh")
        string_7 = string_7.replace("@", "sh")
        string_7 = string_7.replace("5", "ee")
        string_7 = string_7.replace("6", "ea")
        string_7 = string_7.replace("7", "oo")
        string_7 = string_7.replace("8", "ua")
        string_7 = string_7.replace("9", "ou")
        return string_7

    def GetMatrixSyllable(self):
        #no references
        pass

    def GetMatrixGroup(self):
        #no references
        return self.syllableGroups_0.GetMatrix()

    def GetLogins(self, _length:int, count:int):
        return self.syllableGroups_0.GetLogins(_length, count)

    def Save(self, path: str):
        #no references
        pass

    @staticmethod
    def Load(path: str):
        try:
            import json
            json_dict = {}
            with open(path, 'r') as file:
                json_dict = json.load(file)
            
            forSyllableGroups :ForSyllableGroups = ForSyllableGroups.from_json(json_dict)
            # forSyllableGroups :ForSyllableGroups = ForSyllableGroups(**json_dict)

            sEng = SyllableEng()
            sEng.syllableGroups_0 = SyllableGroups()
            sEng.syllableGroups_0.fsg = forSyllableGroups
            return sEng
        except:
            raise

    def GoogleTest(self, letters: str, countUse: str):
        #no references
        pass
        return self.syllableGroups_0.GoogleTest(letters, countUse)