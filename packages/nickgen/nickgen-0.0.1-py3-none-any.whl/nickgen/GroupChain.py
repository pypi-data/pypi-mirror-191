from typing import Dict

class GroupChain:
    def __init__(self, name :str, Name: str):
        self.name = name
        self.Name = Name
        self.forwardGroups :Dict[str,int] = dict()
        self.ForwardGroups :Dict[str,int] = dict()

    def AddForwardGroup(self, group :str):
        if group in self.forwardGroups:
            self.forwardGroups[group] = self.forwardGroups[group] + 1
            self.ForwardGroups[group] = self.ForwardGroups[group] + 1
        else:
            self.forwardGroups[group] = 1
            self.ForwardGroups[group] = 1

    def GetCount(self, group :str):
        if group in self.forwardGroups:
            return self.forwardGroups[group]
        else:
            return 0
