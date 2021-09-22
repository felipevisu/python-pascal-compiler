import string
import sys 

file = open('code1.pas', 'r')
state = 0 
lexeme = []
tokens = []
errors = []
line_index = 0
id_index = 0

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

for line in file:
    line = line.rstrip('\n')
    i = 0
    line_index += 1

    while i < len(line):
        char = line[i]

        if len(errors) > 0:
            print(errors)
            sys.exit()

        if state == 0:
            lexeme.append(char)
            i += 1

            if char in string.ascii_letters:
                state = 1
            elif char in string.digits:
                state = 2
            elif char == '<':
                state = 5
            elif char == '>':
                state = 6
            elif char == '=':
                state = 7
            elif char == '!':
                state = 8
            elif char == ':':
                state = 9
            elif char == '"':
                state = 10
            else:
                state = 0
                word = "".join(lexeme)
                lexeme = []
                token = RESERVED.get(word, None)
                if token:
                    tokens.append(token)
                elif not char.isspace() and char != '.':
                    errors.append((line_index, i))

        # operator or reserved word
        elif state == 1:
            if char in string.ascii_letters or char in string.digits or char == '_':
                state = 1
                lexeme.append(char)
                i += 1
            else:
                state = 0
                word = "".join(lexeme)
                lexeme = []
                token = RESERVED.get(word, None)
                if not token:
                    token = "ID"
                    id_index += 1
                tokens.append(token)

        # integer
        elif state == 2:
            if char in string.digits:
                state = 2
                lexeme.append(char)
                i += 1
            elif char == '.':
                state = 3
                lexeme.append(char)
                i += 1
            else:
                state = 0
                lexeme = []
                tokens.append('INTEGER_CONST')

        # real point
        elif state == 3:
            if char in string.digits:
                state = 4
                i += 1
            else:
                errors.append((line_index, i))
                state = 0
        
        # real digitis
        elif state == 4:
            if char in string.digits:
                state = 4
                i += 1
            else:
                state = 0
                lexeme = []
                tokens.append('FLOAT_CONST')

        # < or <=
        elif state == 5:
            state = 0
            lexeme = []
            if char == '=':
                tokens.append('LTE')
                i += 1
            else:
                tokens.append('LT')

        # > or >=
        elif state == 6:
            state = 0
            lexeme = []
            if char == '=':
                tokens.append('GTE')
                i += 1
            else:
                tokens.append('GT')

        # ==
        elif state == 7:
            state = 0
            lexeme = []
            if char == '=':
                tokens.append('EQUAL')
                i += 1
            else:
                errors.append((line_index, i))
                state = 0

        # !=
        elif state == 8:
            state = 0
            lexeme = []
            if char == '=':
                tokens.append('DIFERENT')
                i += 1
            else:
                errors.append((line_index, i))
                state = 0

        # :=
        elif state == 9:
            state = 0
            lexeme = []
            i += 1
            if char == '=':
                tokens.append('ASSIGN')
            else:
                tokens.append('TWOPOINT')

        # string
        elif state == 10:
            lexeme.append(char)
            i = i+1
            if (
                char in string.ascii_letters
                or char in string.digits
                or char in ['_', ',', '?', '#', ' ']
            ):
                state = 10
            elif char == '"':
                state = 0
                lexeme = []
                tokens.append("STRING_LITERAL")
            else:
                errors.append((line_index, i))
                state = 0


print(tokens)
print(errors)