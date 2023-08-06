from nickgen.ForSyllableGroups import ForSyllableGroups
from nickgen.GroupChain import GroupChain
import random


class SyllableGroups:

    def __init__(self):
        self.fsg: ForSyllableGroups = ForSyllableGroups()
        #self.random_0 = random

    def AddSyllableInGroup(self, group: str, syllable: str):
        if group in self.fsg.syllableGroup:
            self.fsg.syllableGroup[group] = syllable
        else:
            self.fsg.syllableGroup[group] = []

    def AddForwardGroup(self, groupFirst: str, groupSecond: str):
        if groupFirst in self.fsg.forwardGroup:
            self.fsg.forwardGroup[groupFirst].AddForwardGroup(groupSecond)
        else:
            groupChain: GroupChain = GroupChain(groupFirst, groupFirst)
            groupChain.AddForwardGroup(groupSecond)

    def GetMatrix(self):
        # заменить на numpy.array ???
        stringList = []
        numArray = [[], []]

        for key in self.fsg.forwardGroup.keys():
            stringList.append(key)

        for i, item in enumerate(stringList):
            numArray[i] = []

            for i2, item2 in enumerate(stringList):
                numArray[i][i2] = self.fsg.forwardGroup[item].GetCount(item2)
                
        return [stringList, numArray]

    def GetSyllableByGroup(self, group: str):
        if group in self.fsg.syllableGroup:
            return self.fsg.syllableGroup[group]
        return [str]

    def GetGroups(self):
        return self.fsg.syllableGroup.keys()

    def GetLogins(self, length: int, count: int):

        stringList = []
        array = list(self.fsg.syllableGroup.keys())

        for _ in range(count):
            s = ''
            # !!!!!!!!!!!! Check rand(a, b-1)
            index2 = random.randint(0, len(self.fsg.syllableGroup) - 1)
            string_0 = array[index2]
            for _ in range(length):
                s += self.method_2(string_0)
                string_0 = self.method_1(string_0)
            stringList.append(s)

        return stringList

    def method_1(self, string_0: str):
        array1 = list(self.fsg.forwardGroup[string_0].ForwardGroups.values())
        array2 = list(self.fsg.forwardGroup[string_0].ForwardGroups.keys())
        maxValue = 0

        num1 = 0
        for i in range(len(array1) - 1):
            maxValue += array1[i]

        num2 = random.randint(0, maxValue - 1)
        num3 = 0
        for i in range(len(array1) - 1):
            num3 += array1[i]
            if (num1 <= num2 and num2 < num3):
                return array2[i]
            num1 = num3
        return ''

    def method_2(self, string_0: str):
        if string_0 not in self.fsg.syllableGroup:
            return ''
        stringList = self.fsg.syllableGroup[string_0]
        return stringList[random.randint(0, len(stringList)-1)]

    def GoogleTest(self, letters: str, countUse: str):
        # вроде бы не нужен
        pass
