from typing import Pattern, Match
import re
import nickgen.login_macros_handler

class MacrossHandler:

    def __init__(self, openBracket: str, closeBracket: str, execSimlpeMacrossDeligate):
        self.string_0 = 'Difficult macros processing'
        self.string_1 = 'Simple macros processing feature is not assigned'
        self.string_2 = 'Macros parsing'
        self.string_3 = 'Open bracket cutting error'
        self.string_4 = 'Closed bracket cutting error'
        self.string_5 = '{'
        self.DwvbpfyYn = '}'
        self.ExecSimlpeMacrossDeligate = None

        self.string_5 = openBracket
        self.DwvbpfyYn = closeBracket
        self.ExecSimlpeMacrossDeligate = execSimlpeMacrossDeligate
        # self.regex_0 = re.compile(re.escape(self.string_5) + "[\\w\\W]*?" + re.escape(self.DwvbpfyYn))
        self.regex_0 = re.compile(re.escape(self.string_5) + "[\\w\\W]*?" + re.escape(self.DwvbpfyYn))

    def ExecComplexMacross(self, value :str):
        
        # if self.ExecSimlpeMacrossDeligate is None:
        #     return ''
        
        if not value:
            return ''

        s = value
        _input =''
        while s != _input:
            #_input =''
            s = self.regex_0.sub(self.method_0, s)
            _input = s
        return s


    
    def method_0(self, match :Match):

        str1 = ''
        str2 = ''
        try:
            # возможен баг. возможно надо в слайсинге добавить -1 на конце
            str2 = match.group(0)[len(self.string_5) : len(match.group(0)) - len(self.string_5)]
        except:
            return ''

        str3 = self.ExecComplexMacross(str(str2))
        if not (str3 == str2):
            return self.string_5 + str3
        
        str4 = ''
        try:
            #str4 = str2[0 : len(str2) - len(self.DwvbpfyYn)]
            str4 = str2[0 : len(str2)]
        except:
            return ''
        
        str1 = nickgen.login_macros_handler.LoginMacrossHandler.ExecSimplMacross(str(str4))
        return str1

    def SetExecSimlpeMacrossDeligate(self, delegate):
        self.ExecSimlpeMacrossDeligate = delegate
