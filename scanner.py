import sys
import string

from prettytable import PrettyTable

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
    'read': 'READ',
    'print': 'PRINT',
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

class Token:
    def __init__(self, token, value, row):
        self.token = token
        self.value = value
        self.row = row


class Scanner:
    def __init__(self, file_path):
        self.file = open(file_path, 'r')
        self.data = None
        self.errors = []
        self.tokens = []
        self.lexeme = []
        self.state = 0

    def get_word(self):
        return "".join(self.lexeme)

    def clean_lexeme(self):
        self.lexeme = []

    def printter(self):
        x = PrettyTable()
        x.field_names = ["Token", "Valor", "Linha"]
        x.add_rows(
            [
                [token.token, token.value, token.row] for token in self.tokens
            ]
        )
        print(x)

    def scan(self):
        row = 0

        for line in self.file:
            line = line.rstrip('\n')
            i = 0
            row += 1

            while i < len(line):
                char = line[i]

                if len(self.errors) > 0:
                    print(self.errors)
                    sys.exit()

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
                        word = self.get_word()
                        self.clean_lexeme()
                        token = RESERVED.get(word, None)
                        if token:
                            self.state = 0
                            self.tokens.append(Token(token, word, row))
                        elif not char.isspace() and char != '.':
                            self.errors.append((row, i))

                # operator or reserved word
                elif self.state == 1:
                    if char in string.ascii_letters or char in string.digits or char == '_':
                        self.state = 1
                        self.lexeme.append(char)
                        i += 1
                    else:
                        self.state = 0
                        word = self.get_word()
                        self.clean_lexeme()
                        token = RESERVED.get(word, None)
                        if not token:
                            token = "ID"
                        self.tokens.append(Token(token, word, row))

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
                        word = self.get_word()
                        self.clean_lexeme()
                        token = 'INTEGER_CONST'
                        self.tokens.append(Token(token, word, row))

                # real point
                elif self.state == 3:
                    self.lexeme.append(char)
                    if char in string.digits:
                        self.state = 4
                        i += 1
                    else:
                        self.errors.append((row, i))

                # real digitis
                elif self.state == 4:
                    self.lexeme.append(char)
                    if char in string.digits:
                        self.state = 4
                        i += 1
                    else:
                        self.state = 0
                        word = self.get_word()
                        self.clean_lexeme()
                        token = 'FLOAT_CONST'
                        self.tokens.append(Token(token, word, row))

                # < or <=
                elif self.state == 5:
                    self.state = 0
                    if char == '=':
                        token = 'LTE'
                        i += 1
                    else:
                        token = 'LT'
                    word = self.get_word()
                    self.clean_lexeme()
                    self.tokens.append(Token(token, word, row))

                # > or >=
                elif self.state == 6:
                    self.state = 0
                    if char == '=':
                        token = 'GTE'
                        i += 1
                    else:
                        token = 'GT'
                    word = self.get_word()
                    self.clean_lexeme()
                    self.tokens.append(Token(token, word, row))

                # ==
                elif self.state == 7:
                    self.state = 0
                    word = self.get_word()
                    self.clean_lexeme()
                    if char == '=':
                        token = 'EQUAL'
                        self.tokens.append(Token(token, word, row))
                        i += 1
                    else:
                        self.errors.append((row, i))

                # !=
                elif self.state == 8:
                    self.state = 0
                    word = self.get_word()
                    self.clean_lexeme()
                    if char == '=':
                        token = 'DIFERENT'
                        self.tokens.append(Token(token, word, row))
                        i += 1
                    else:
                        self.errors.append((row, i))

                # :=
                elif self.state == 9:
                    self.lexeme.append(char)
                    word = self.get_word()
                    self.clean_lexeme()
                    self.state = 0
                    i += 1
                    if char == '=':
                        token = 'ASSIGN'
                    else:
                        token = 'TWOPOINT'
                    self.tokens.append(Token(token, word, row))

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
                        word = self.get_word()
                        self.clean_lexeme()
                        token = "STRING_LITERAL"
                        self.tokens.append(Token(token, word, row))
                    else:
                        self.errors.append((row, i))
