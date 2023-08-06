from typing import Dict


class SyllableChain:

    def __init__(self, name: str):
        self.dictionary_0: Dict[str,int] = Dict()
        self.string_0: str = name

        #properties
        self.Name: str
        self.ForwardSyllables: Dict[str,int]

    def AddForwardSyllable(self, syllable: str):
        if syllable in self.dictionary_0:
            self.dictionary_0[syllable] = self.dictionary_0[syllable] + 1
        else:
            self.dictionary_0[syllable] = 1

    def GetCount(self, syllable: str):
        if syllable in self.dictionary_0:
            return self.dictionary_0[syllable]
        return 0