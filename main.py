import string

file = open('code.c', 'r')
state = 0 
lexeme = []
tokens = []
line_number = 1
special = ['(', ')', '{', '}', ',', ';', '+', '-', '*', '/', ' ', '\n', '\t']

RESERVED = {
    'main': 'MAIN',
    'int': 'INT',
    'float': 'FLOAT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'read': 'READ',
    'print': 'PRINT',
    '(': 'LBRACKET',
    ')': 'RBRACKET',
    '{': 'LBRACE',
    '}': 'RBRACE',
    ',': 'COMMA',
    ';': 'PCOMMA',
    '=': 'ATTR',
    '<': 'LT',
    '<=': 'LTE',
    '>': 'GT',
    '>=': 'GTE',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULT',
    '/': 'DIV',
    '[': 'LCOL',
    ']': 'RCOL'
}

for line in file:
    line = line.rstrip('\n')
    
    for char in line:
        
        if state == 0:
            if char in string.ascii_letters:
                state = 1
                lexeme.append(char)
            elif char in string.digits:
                state = 2
            elif char == '>':
                state = 6
            elif char == '<':
                state = 5

        elif state == 1:
            if char in string.ascii_letters or char in string.digits:
                state = 1
                lexeme.append(char)
            else:
                state = 0

        elif state == 2:
            if char in string.digits:
                state = 2
            elif char == '.':
                state = 3
            else:
                state = 0

        elif state == 3:
            if char in string.digits:
                state = 4
        
        elif state == 4:
            if char in string.digits:
                state = 4
            else:
                state = 0

        elif state == 5:
            if char == '=':
                state = 0
            else:
                state = 0

        elif state == 6:
            if char == '=':
                state = 0
            else:
                state = 0
            
    line_number += 1