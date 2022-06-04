# package DevProgLang/Tokens.py
INT = 'INT'
FLOAT = 'FLOAT'
ID = 'VAR'
OP = '_OP'
KW = 'KW_'

# Token's List
token_exprs = [
    (r'[\n]+', 'NEWLINE'),
    (r'[ \t]+', None),
    (r'#.*', 'COMMENT'),
    (r'[/]\*([^#]*)\*[/]', 'MULTILINE_COMMENT'),
    (r'[-]*[0-9]+\.[0-9]+', FLOAT),
    (r'[-]*[1-9]+[0-9]*|0', INT),
    (r'\'', 'MARKS'),
    (r'\"', 'DOUBLE_QUOTES'),
    (r'\(', 'L_BRACKET'),
    (r'\)', 'R_BRACKET'),
    (r'\{', 'L_BRACE'),
    (r'\}', 'R_BRACE'),
    (r'\[', 'L_SQUARE_BRACKET'),
    (r'\]', 'R_SQUARE_BRACKET'),
    (r'%', 'MOD' + OP),
    (r'//', 'DIV' + OP),
    (r'\+', 'PLUS' + OP),
    (r'-', 'MINUS' + OP),
    (r'\*\*', 'EXPONENTIATION' + OP),
    (r'\*', 'MULTIPLICATION' + OP),
    (r'/', 'SLASH' + OP),
    (r'input|<<', KW + 'INPUT'),
    (r'print|>>', KW + 'PRINT'),
    (r'<=', 'LESS_EQUALLY'),
    (r'<', 'LESS'),
    (r'>=', 'MORE_EQUALLY'),
    (r'>', 'MORE'),
    (r'==', 'EQUALS'),
    (r':=|=', 'ASSIGN'),
    (r'!=', 'NOT_EQUALLY'),
    (r'\:', 'COLON'),
    (r'\;', 'SEMICOLON'),
    (r'true', KW + 'TRUE'),
    (r'false', KW + 'FALSE'),
    (r'int', KW + 'INT'),
    (r'str', KW + 'STR'),
    (r'float', KW + 'FLOAT'),
    (r'bool', KW + 'BOOL'),
    (r'and', KW + 'AND'),
    (r'or', KW + 'OR'),
    (r'not', KW + 'NOT'),
    (r'if', KW + 'IF'),
    (r'in', KW + 'IN'),
    (r'is', KW + 'IS'),
    (r'then', KW + 'THEN'),
    (r'else', KW + 'ELSE'),
    (r'while', KW + 'WHILE'),
    (r'for', KW + 'FOR'),
    (r'do', KW + 'DO'),
    (r'begin', KW + 'begin'),
    (r'end', KW + 'END'),
    (r'exit', KW + 'EXIT'),
    (r'func', KW + 'FUNC'),
    (r'List', KW + 'LIST'),
    (r'.pop', 'LL_POP'),
    (r'.len', 'LL_LEN'),
    (r'.insertAtEnd', 'LL_INSERT_END'),
    (r'.insertAtHead', 'LL_INSERT_HEAD'),
    (r'.deleteAtHead', 'LL_DELETE_HEAD'),
    (r'.delete', 'LL_DELETE'),
    (r'.search', 'LL_SEARCH'),
    (r'.isEmpty', 'LL_IS_EMPTY'),
    (r'\.', 'POINT'),
    (r'\,', 'COMMA'),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]


class Token:

    def __init__(self, type_token, value, number_line, position):
        self.type_token = type_token
        self.value = value
        self.number_line = number_line
        self.position = position

    def getTypeToken(self):
        return self.type_token

    def getValue(self):
        return self.value

    def getNumberLine(self):
        return self.number_line

    def getPosition(self):
        return self.position

    def toString(self):  # Output
        if self.getTypeToken() != 'NEWLINE':
            text = f">>> [type: {self.type_token}; " \
                   f"value: '{self.value}'; " \
                   f"number_line: {self.number_line}; " \
                   f"position: {self.position}]"
        else:
            text = f">>> [type: {self.type_token}; " \
                   f"number_line: {self.number_line}; " \
                   f"position: {self.position}]"
        print(text)
