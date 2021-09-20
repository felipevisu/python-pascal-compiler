import string
import re

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
    i = 0

    while i < len(line):
        char = line[i]

        if state == 0:
            if char in string.ascii_letters:
                state = 1
                lexeme.append(char)
                i += 1
            elif char in string.digits:
                state = 2
                lexeme.append(char)
                i += 1
            elif char == '>':
                state = 6
                lexeme.append(char)
                i += 1
            elif char == '<':
                state = 5
                lexeme.append(char)
                i += 1

        elif state == 1:
            if char in string.ascii_letters or char in string.digits:
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
        
        elif state == 4:
            if char in string.digits:
                state = 4
                i += 1
            else:
                state = 0
                lexeme = []
                tokens.append('FLOAT_CONST')

        elif state == 5:
            if char == '=':
                state = 0
                lexeme = []
                tokens.append('LTE')
                i += 1
            else:
                state = 0
                lexeme = []
                tokens.append('LT')

        elif state == 6:
            if char == '=':
                state = 0
                lexeme = []
                tokens.append('GTE')
                i += 1
            else:
                state = 0
                lexeme = []
                tokens.append('GT')
            
    line_number += 1