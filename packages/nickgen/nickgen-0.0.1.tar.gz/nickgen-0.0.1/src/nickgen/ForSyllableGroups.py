from typing import DefaultDict, Dict

from nickgen.GroupChain import GroupChain


class ForSyllableGroups:
    def __init__(self):
        # <str,List<str>>
        self.syllableGroup = {}
        # <str,GroupChain>
        self.forwardGroup = {}

        # Dictionary<string, List<string>> syllableGroup = new Dictionary<string, List<string>>();
        # Dictionary<string, GroupChain> forwardGroup = new Dictionary<string, GroupChain>();

    @classmethod
    def from_json(cls, data):
        # import json
        # fp = open('test.json', 'w')
        # json.dump(data, fp, indent=4)
        # fp.close()
        try:
            result = ForSyllableGroups()
            # result = cls.__new__(cls)

            # result.syllableGroup = Dict()
            # result.forwardGroup = Dict()

            syllableGroup_item = data["syllableGroup"]
            for key in syllableGroup_item.keys():
                value = syllableGroup_item[key]
                result.syllableGroup[key] = value

            forwardGroup_item = data["forwardGroup"]
            for key in forwardGroup_item.keys():
                value = forwardGroup_item[key]
                # value1 = value["forwardGroups"]
                value1_obj_dict = value["forwardGroups"]
                value1_obj_name = value["name"]
                value1_obj_Name = value["Name"]
                value1_obj_Dict = value["ForwardGroups"]

                gChainObj = GroupChain(value1_obj_name, value1_obj_Name)
                gChainObj.forwardGroups = value1_obj_dict
                gChainObj.ForwardGroups = value1_obj_Dict

                result.forwardGroup[key] = gChainObj

            return result
        except:
            raise
