import string

file = open('code.pas', 'r')
state = 0 
lexeme = []
tokens = []

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
    ':': 'COLON',
    ':=': 'ATTR',
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

    while i < len(line):
        char = line[i]

        if state == 0:
            lexeme.append(char)
            i += 1

            if char in string.ascii_letters:
                state = 1
            elif char in string.digits:
                state = 2
            elif char == '>':
                state = 6
            elif char == '<':
                state = 5
            elif char == '=':
                state = 7
            elif char == '!':
                state = 8
            elif char == ':':
                state = 9
            else:
                state = 0
                word = "".join(lexeme)
                lexeme = []
                token = RESERVED.get(word, None)
                tokens.append(token) if token else None

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
                tokens.append(token) if token else tokens.append('ID')

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

        elif state == 3:
            if char in string.digits:
                state = 4
                i += 1
            else:
                # error
                pass
        
        elif state == 4:
            if char in string.digits:
                state = 4
                i += 1
            else:
                state = 0
                lexeme = []
                tokens.append('FLOAT_CONST')

        elif state == 5:
            state = 0
            lexeme = []
            if char == '=':
                tokens.append('LTE')
                i += 1
            else:
                tokens.append('LT')

        elif state == 6:
            state = 0
            lexeme = []
            if char == '=':
                tokens.append('GTE')
                i += 1
            else:
                tokens.append('GT')

        elif state == 7:
            state = 0
            lexeme = []
            if char == '=':
                tokens.append('EQUAL')
                i += 1
            else:
                # error
                pass

        elif state == 8:
            state = 0
            lexeme = []
            if char == '=':
                tokens.append('DIFERENT')
                i += 1
            else:
                # error
                pass

        elif state == 9:
            state = 0
            lexeme = []
            i += 1
            if char == '=':
                tokens.append('ATTR')
            else:
                tokens.append('COLLON')

print(tokens)