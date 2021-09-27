import re


class lexerCl(object):
    token = {"IF": "^if$", "ELSE": "^else$", "WHILE": "^while$","OP": "^[-+*/]$", "LOGICAL_OP": r"^==|>|>=|<|<=|!=$","LBreaket": "[(]", "RBreaket": "[)]", 'POINT': r'\.',"END_COM": "^;$", "LFBreaket": "^[{]$",'LINKED_LIST_KW': r'LinkedList',"RFBreaket": "^[}]$", "ASSIGN_OP": "^=$","ENDCOM": "^;$", "NUMBER": r"^0|([1-9][0-9]*)$","STR": r"'[^']*'", "VAR": "^[a-zA-Z0-9_]+$","UNDEFINED": r".*[^.]*"}

    def __init__(self):
        self.list_tokens = []

    def __token_setter(self, item):
        for key in self.token.keys():
            if re.fullmatch(self.token[key], item):
                return key

    def term_getter(self, file):
        with open(file) as file_handler:
            buffer = ''
            last_token = ''
            for line in file_handler:
                for char in line:
                    if not len(buffer) and char == "'":
                        buffer += char
                        continue
                    elif len(buffer) and not buffer.count("'") == 2:
                        if buffer[0] == "'":
                            buffer += char
                            continue
                    if last_token == 'POINT':
                        if not char == '(':
                            buffer += char
                            continue
                        else:
                            self.list_tokens.append({'METHOD': buffer})
                            buffer = ''
                    last_token = self.__token_setter(buffer)
                    buffer += char
                    token = self.__token_setter(buffer)
                    if token == "UNDEFINED":
                        if len(buffer) and not last_token == "UNDEFINED":
                            self.list_tokens.append({last_token: buffer[:-1]})
                        if not (buffer[-1] == ' ' or buffer[-1] == '\n'):
                            buffer = buffer[-1]
                        else:
                            buffer = ''

            token = self.__token_setter(buffer)
            if not token == "UNDEFINED":
                self.list_tokens.append({token: buffer[0]})