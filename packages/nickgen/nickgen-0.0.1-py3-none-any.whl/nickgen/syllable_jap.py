import random
import re
from typing import Dict, List

from nickgen.syllable_chain import SyllableChain


class SyllableJap:

    def __init__(self):
        #constants
        self.string_0 = 'VoidSyllable'
        self.string_1 = 'VoidGroup'

        self.string_2 = ['ka', 'ki', 'ku', 'ke', 'ko', 'kya', 'kyu', 'kyo', 'sa', 'shi', 'su', 'se', 'so', 'sha', 'shu', 'sho', 'ta', 'chi', 'tsu', 'te', 'to', 'cha', 'chu', 'cho', 'na', 'ni', 'nu', 'ne', 'no', 'nya', 'nyu', 'nyo', 'ha', 'hi', 'fu', 'he', 'ho', 'hya', 'hyu', 'hyo', 'ma', 'mi', 'mu', 'me', 'mo', 'mya', 'myu', 'myo', 'ya', 'yu', 'yo', 'ra', 'ri', 'ru', 're', 'ro', 'rya', 'ryu', 'ryo', 'wa', 'wi', 'we', 'wo', 'ga', 'gi', 'gu', 'ge', 'go', 'gya', 'gyu', 'gyo', 'za', 'ji', 'zu', 'ze', 'zo', 'ja', 'ju', 'jo', 'da', 'ji', 'dzu', 'de', 'do', 'ja', 'ju', 'jo', 'ba', 'bi', 'bu', 'be', 'bo', 'bya', 'byu', 'byo', 'pa', 'pi', 'pu', 'pe', 'po', 'pya', 'pyu', 'pyo', 'a', 'i', 'u', 'e', 'o', 'n', 'vu']
        self.string_3 = ['か', 'き', 'く', 'け', 'こ', 'きゃ', 'きゅ', 'きょ', 'さ', 'し', 'す', 'せ', 'そ', 'しゃ', 'しゅ', 'しょ', 'た', 'ち', 'つ', 'て', 'と', 'ちゃ', 'ちゅ', 'ちょ', 'な', 'に', 'ぬ', 'ね', 'の', 'にゃ', 'にゅ', 'にょ', 'は', 'ひ', 'ふ', 'へ', 'ほ', 'ひゃ', 'ひゅ', 'ひょ', 'ま', 'み', 'む', 'め', 'も', 'みゃ', 'みゅ', 'みょ', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'りゃ', 'りゅ', 'りょ', 'わ', 'ゐ', 'ゑ', 'を', 'が', 'ぎ', 'ぐ', 'げ', 'ご', 'ぎゃ', 'ぎゅ', 'ぎょ', 'ざ', 'じ', 'ず', 'ぜ', 'ぞ', 'じゃ', 'じゅ', 'じょ', 'だ', 'ぢ', 'づ', 'で', 'ど', 'ぢゃ', 'ぢゅ', 'ぢょ', 'ば', 'び', 'ぶ', 'べ', 'ぼ', 'びゃ', 'びゅ', 'びょ', 'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ', 'ぴゃ', 'ぴゅ', 'ぴょ', 'あ', 'い', 'う', 'え', 'お', 'ん', 'ゔ']
        self.string_4 = '(?<=\\s)[かきくけこきゃきゅきょさしすせそしゃしゅしょたちつてとちゃちゅちょなにぬねのにゃにゅにょはひふへほひゃひゅひょまみむめもみゃみゅみょやゆよらりるれろりゃりゅりょわゐゑをがぎぐげごぎゃぎゅぎょざじずぜぞじゃじゅじょだぢづでどぢゃぢゅぢょばびぶべぼびゃびゅびょぱぴぷぺぽぴゃぴゅぴょあいうえおんゔ]+'
        self.sortedList_0 = []
        self.dictionary_0 :Dict[str,SyllableChain] = dict()
        self.arrayList_0 = None

    def GetJapWord(self, countOfBlocks:int):
        empty = ''
        for _ in range(countOfBlocks):
            empty += self.string_2[random.randint(0, len(self.string_2) - 1)]
        return empty

    def AddText(self, text:str):
        matches = re.findall(self.string_4, text)
        if len(matches) <= 0:
            return
        for capture in matches:
            self.method_1(capture)

    def method_1(self, string_5 :str):
        if not string_5:
            return
        
        stringList = []
        flag1 = False
        while not flag1 and string_5:
            flag2 = False
            for index in range(len(self.string_3)):
                if string_5.startswith(self.string_3[index]):
                    if self.string_3[index] != 'う':
                        stringList.append(self.string_2[index])
                    string_5 = string_5[0:len(self.string_3[index])]
                    flag2 = True
                    break
            if not flag2:
                flag1 = True
        
        key = ''.join(stringList)
        for tup in self.sortedList_0:
            if key == tup[0]:
                return

        # что-то неправильно?
        if key in self.sortedList_0:
            return
        self.sortedList_0.append((key, False))
        self.sortedList_0 = sorted(self.sortedList_0, key=lambda x: x[0])
        stringList.append('VoidSyllable')

        for i, item in enumerate(stringList[:-1]):
            if item in self.dictionary_0:
                self.dictionary_0[item].AddForwardSyllable(stringList[i + 1])
            else:
                #syllableChain = SyllableChain(item)
                pass

    def GetMatrixSyllable(self):
        stringList :List[str]= List()
        numArray = [ [],[] ]

        for key in self.dictionary_0.keys():
            stringList.append(key)
        
        for i, item in enumerate(stringList):
            numArray[i] = []

            for i2, item2 in enumerate(stringList):
                numArray[i][i2] = self.dictionary_0[item].GetCount(item2)

        arrayList = []
        arrayList.append(stringList)
        arrayList.append(numArray)
        self.arrayList_0 = arrayList
        return arrayList

    def GetLogins(self, lenght :int, count : int):
        if self.arrayList_0 is None:
            self.arrayList_0 = self.GetMatrixSyllable()
        
        stringList :List[str] = []
        strArray = list(self.arrayList_0[0])
        numArray = self.arrayList_0[1]

        for _ in range(count):
            str1 = ''
            index2 = random.randint(0, len(strArray) - 1)
            str2 = str1 + strArray[index2]
            for _ in range(lenght -1):
                maxValue = 0
                num1 = 0
                for index4 in range(len(numArray) -1):
                    maxValue += numArray[index2][index4]
                num2 = random.randint(0, maxValue - 1)
                num3 = 0
                for index4 in range(len(numArray) -1):
                    num3 += numArray[index2][index4]
                    if num1 > num2 or num2 >= num3:
                        num1 = num3
                    else:
                        index2 = index4
                        break
                str2 += strArray[index2]
            stringList.append(str2)
        return stringList

    def Save(self, path :str):
        #no references
        pass

    @staticmethod
    def Load(path :str):
        try:
            import json
            json_dict = {}
            with open(path, 'r') as file:
                json_dict = json.load(file)
            
            # arrayList = SyllableJap.arrayList_from_json(json_dict)
            arrayList = json_dict
            sJap = SyllableJap()
            sJap.arrayList_0 = arrayList
            return sJap
        except:
            #костыль!
            raise
            #raise Exception('Cant load SyllableJap')
        

    @classmethod
    def arrayList_from_json(cls, data):
        # import json
        # fp = open('test.json', 'w')
        # json.dump(data, fp, indent=4)
        # fp.close()
        try:
            result = []

            
            return result
        except:
            raise
            #raise Exception('Error loading arrayList_from_json()')