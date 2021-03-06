import string

from prettytable import PrettyTable
from utils import Error

RESERVED = {
    'program': 'PROGRAM',
    'begin': 'BEGIN',
    'end': 'END',
    'var': 'VAR',
    'boolean': 'BOOLEAN',
    'integer': 'INTEGER',
    'real': 'REAL',
    'string': 'STRING',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'do': 'DO',
    'to': 'TO',
    'read': 'READ',
    'write': 'WRITE',
    'true': 'TRUE',
    'false': 'FALSE',
    '(': 'LBRACKET',
    ')': 'RBRACKET',
    '{': 'LBRACE',
    '}': 'RBRACE',
    '[': 'LCOL',
    ']': 'RCOL',
    ',': 'COMMA',
    ';': 'PCOMMA',
    ':': 'TWOPOINT',
    ':=': 'ASSIGN',
    '==': 'EQUAL',
    '!=': 'DIFERENT',
    '<': 'LT',
    '<=': 'LTE',
    '>': 'GT',
    '>=': 'GTE',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULT',
    '/': 'DIV',
}

RESERVED_REVERSED = {v: k for k, v in RESERVED.items()}

class Token:
    def __init__(self, type, lexeme, row):
        self.type = type
        self.lexeme = lexeme
        self.row = row

    def __str__(self):
        return f'Type: {self.type}, Lexeme: {self.lexeme}, Row: {self.lexeme}'


class Scanner:
    def __init__(self, file_path):
        self.file = open(file_path, 'r')
        self.data = None
        self.errors = []
        self.tokens = []
        self.lexeme = []
        self.state = 0

    def get_lexeme(self):
        return "".join(self.lexeme)

    def clean_lexeme(self):
        self.lexeme = []

    def printter(self):
        tokens = PrettyTable()
        tokens.field_names = ["Type", "Lexeme", "Row"]
        tokens.add_rows([
            [token.type, token.lexeme, token.row] for token in self.tokens
        ])
        return tokens

    def scan(self):
        row = 0

        for line in self.file:
            line = line.rstrip('\n')
            i = 0
            row += 1

            while i < len(line):
                char = line[i]

                if self.state == 0:
                    self.lexeme.append(char)
                    i += 1

                    if char in string.ascii_letters:
                        self.state = 1
                    elif char in string.digits:
                        self.state = 2
                    elif char == '<':
                        self.state = 5
                    elif char == '>':
                        self.state = 6
                    elif char == '=':
                        self.state = 7
                    elif char == '!':
                        self.state = 8
                    elif char == ':':
                        self.state = 9
                    elif char == '"':
                        self.state = 10
                    else:
                        lexeme = self.get_lexeme()
                        self.clean_lexeme()
                        type = RESERVED.get(lexeme, None)
                        if type:
                            self.state = 0
                            self.tokens.append(Token(type, lexeme, row))
                        elif not char.isspace() and char != '.':
                            self.errors.append(Error(lexeme, row, 'Lexical error'))

                # operator or reserved word
                elif self.state == 1:
                    if char in string.ascii_letters or char in string.digits or char == '_':
                        self.state = 1
                        self.lexeme.append(char)
                        i += 1
                    else:
                        self.state = 0
                        lexeme = self.get_lexeme()
                        self.clean_lexeme()
                        type = RESERVED.get(lexeme, None)
                        if not type:
                            type = "ID"
                        self.tokens.append(Token(type, lexeme, row))

                # integer
                elif self.state == 2:
                    if char in string.digits:
                        self.state = 2
                        self.lexeme.append(char)
                        i += 1
                    elif char == '.':
                        self.state = 3
                        self.lexeme.append(char)
                        i += 1
                    else:
                        self.state = 0
                        lexeme = self.get_lexeme()
                        self.clean_lexeme()
                        type = 'INTEGER_CONST'
                        self.tokens.append(Token(type, lexeme, row))

                # real point
                elif self.state == 3:
                    self.lexeme.append(char)
                    if char in string.digits:
                        self.state = 4
                        i += 1
                    else:
                        self.errors.append(Error(lexeme, row, 'Lexical error'))

                # real digitis
                elif self.state == 4:
                    self.lexeme.append(char)
                    if char in string.digits:
                        self.state = 4
                        i += 1
                    else:
                        self.state = 0
                        lexeme = self.get_lexeme().replace(';', '')
                        self.clean_lexeme()
                        type = 'FLOAT_CONST'
                        self.tokens.append(Token(type, lexeme, row))

                # < or <=
                elif self.state == 5:
                    self.state = 0
                    if char == '=':
                        type = 'LTE'
                        i += 1
                    else:
                        type = 'LT'
                    lexeme = self.get_lexeme()
                    self.clean_lexeme()
                    self.tokens.append(Token(type, lexeme, row))

                # > or >=
                elif self.state == 6:
                    self.state = 0
                    if char == '=':
                        type = 'GTE'
                        i += 1
                    else:
                        type = 'GT'
                    lexeme = self.get_lexeme()
                    self.clean_lexeme()
                    self.tokens.append(Token(type, lexeme, row))

                # ==
                elif self.state == 7:
                    self.state = 0
                    lexeme = self.get_lexeme()
                    self.clean_lexeme()
                    if char == '=':
                        type = 'EQUAL'
                        self.tokens.append(Token(type, lexeme, row))
                        i += 1
                    else:
                        self.errors.append(Error(lexeme, row, 'Lexical error'))

                # !=
                elif self.state == 8:
                    self.state = 0
                    lexeme = self.get_lexeme()
                    self.clean_lexeme()
                    if char == '=':
                        type = 'DIFERENT'
                        self.tokens.append(Token(type, lexeme, row))
                        i += 1
                    else:
                        self.errors.append(Error(lexeme, row, 'Lexical error'))

                # :=
                elif self.state == 9:
                    self.lexeme.append(char)
                    lexeme = self.get_lexeme()
                    self.clean_lexeme()
                    self.state = 0
                    i += 1
                    if char == '=':
                        type = 'ASSIGN'
                    else:
                        type = 'TWOPOINT'
                    self.tokens.append(Token(type, lexeme, row))

                # string
                elif self.state == 10:
                    self.lexeme.append(char)
                    i = i+1
                    if (
                        char in string.ascii_letters
                        or char in string.digits
                        or char in ['_', ',', '?', '#', ' ']
                    ):
                        self.state = 10
                    elif char == '"':
                        self.state = 0
                        lexeme = self.get_lexeme()
                        self.clean_lexeme()
                        type = "STRING_LITERAL"
                        self.tokens.append(Token(type, lexeme, row))
                    else:
                        self.errors.append(Error(lexeme, row, 'Lexical error'))