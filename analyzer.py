from inspect import currentframe, getframeinfo
from prettytable import PrettyTable


class Error:
    def __init__(self, token, row, message):
        self.token = token
        self.row = row
        self.message = message

    def __str__(self):
        return f'Item: {self.token}, Row: {self.row}, Message: {self.message}'


class Symble:
    def __init__(self, name, type, address):
        self.name = name
        self.type = type
        self.value = 0
        self.address = address

    def __str__(self):
        return f'Name: {self.name}, Type: {self.type}, Address: {self.address}'


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = tokens[0]
        self.index = 0
        self.size = len(tokens)
        self.errors = []
        self.symtable = []
        self.address = 0

    def match(self, token):
        caller = currentframe().f_back
        function = getframeinfo(caller)[2]
        if self.current.type == token:
            print(f'Match {token} in {function}')
            self.index += 1
            if self.index < self.size:
                self.current = self.tokens[self.index]
        else:
            error = Error(token, self.current.row, 'Syntax error')
            self.errors.append(error)

    def add_symble(self, symble):
        for item in self.symtable:
            if item.name == symble.name:
                self.errors.append(Error(symble.name, self.current.row, 'Variable already declared'))
        self.symtable.append(symble)

    def check_symble(self, lexeme):
        for symble in self.symtable:
            if symble.name == lexeme:
                return
        self.errors.append(Error(lexeme, self.current.row, 'Undeclared variable'))

    def printter(self):
        symtable = PrettyTable()
        symtable.field_names = ["Name", "Type", "Address"]
        symtable.add_rows([
            [symble.name, symble.type, symble.address] for symble in self.symtable
        ])
        print(symtable)

        errors = PrettyTable()
        errors.field_names = ["Value", "Row", "Message"]
        errors.add_rows([
            [error.token, error.row, error.message] for error in self.errors
        ])
        print(errors)

    def parse(self):
        self.program()
        self.printter()
            
    def program(self):
        if self.current.type == 'PROGRAM':
            self.match('PROGRAM')
            self.match('ID')
            self.match('PCOMMA')
            self.declarations()

    def declarations(self):
        self.declared_variables()

    def declared_variables(self):
        if self.current.type == 'VAR':
            self.match('VAR')
        else:
            self.begin()
            return

        while True:
            if self.current.type == 'ID':
                symble = Symble(self.current.lexeme, 'EMPTY', self.address)
                self.add_symble(symble)
                self.address += 4
                self.match('ID')
            if self.current.type == 'COMMA':
                self.match('COMMA')
            if self.current.type == 'TWOPOINT':
                self.match('TWOPOINT')
                break

        if self.current.type == 'REAL':
            for vars in self.symtable:
                if vars.type == 'EMPTY':
                    vars.type = 'REAL'
            self.match('REAL')

        if self.current.type == 'INTEGER':
            for vars in self.symtable:
                if vars.type == 'EMPTY':
                    vars.type = 'INTERGER'
            self.match('INTEGER')

        if self.current.type == 'STRING':
            for vars in self.symtable:
                if vars.type == 'EMPTY':
                    vars.type = 'STRING'
            self.match('STRING')

        if self.current.type == 'BOOLEAN':
            for vars in self.symtable:
                if vars.type == 'EMPTY':
                    vars.type = 'BOOLEAN'
            self.match('BOOLEAN')

        if self.current.type == 'PCOMMA':
            self.match('PCOMMA')

        self.declared_variables()

    def begin(self):
        if self.current.type == 'BEGIN':
            self.match('BEGIN')

            while self.current.type != 'END':
                self.statements()

            if self.current.type == 'END':
                pass

    def statements(self):
        while True:
            if self.current.type == 'IF':
                self.if_statement()
            elif self.current.type == 'FOR':
                self.for_statement()
            elif self.current.type == 'WHILE':
                self.while_statement()
            elif self.current.type  == 'PRINT':
                self.print()
            elif self.current.type  == 'READ':
                self.read()
            elif self.current.type == 'ID':
                self.check_symble(self.current.lexeme)
                self.match('ID')

            if self.current.type == 'LBRACKET':
                self.match('LBRACKET')
                self.factor()
                self.match('RBRACKET')
            if self.current.type == 'ASSIGN':
                self.match('ASSIGN')

            self.logic()

            if self.current.type == 'PCOMMA':
                self.match('PCOMMA')

            if self.current.type == 'END':
                if self.index < self.size:
                    self.match('END')
                else:
                    break

            if self.current.type == 'ELSE':
                return

            if self.current.type == 'TO':
                return

    def for_statement(self):
        self.match('FOR')
        self.statements()
        self.match('TO')
        self.factor()
        self.match('DO')
        self.statements()

    def while_statement(self):
        self.match('WHILE')
        self.logic()
        self.match('DO')
        self.statements()

    def if_statement(self):
        self.match('IF')
        self.logic()
        self.match('THEN')
        self.statements()

        if self.current.type == 'ELSE':
            self.match('ELSE')
            self.statements()

    def print(self):
        self.match('PRINT')
        self.logic()
        self.match('PCOMMA')

    def read(self):
        self.match('READ')
        self.match('ID')
        self.match('PCOMMA')

    def logic(self):
        if self.current.type == 'LT':
            self.match('LT')
            self.expression()
        elif self.current.type == 'GT':
            self.match('GT')
            self.expression()
        elif self.current.type == 'LTE':
            self.match('LTE')
            self.expression()
        elif self.current.type == 'GTE':
            self.match('GTE')
            self.expression()
        elif self.current.type == '==':
            self.match('==')
            self.expression()
        elif self.current.type == 'DIFERENT':
            self.match('DIFERENT')
            self.expression()
        else:
            self.expression()

    def expression(self):
        self.term()
        self.expression_prime()
    
    def term(self):
        self.factor()
        self.term_prime()

    def expression_prime(self):
        if self.current.type == 'PLUS':
            self.match('PLUS')
            self.term()
            self.expression_prime()
        elif self.current.type == 'MINUS':
            self.match('MINUS')
            self.term()
            self.expression_prime()

    def factor(self):
        if self.current.type == 'ID':
            self.match('ID')
            return

        if self.current.type == 'STRING_LITERAL':
            self.match('STRING_LITERAL')
            return

        if self.current.type == 'INTEGER_CONST':
            self.match('INTEGER_CONST')
            return

        if self.current.type == 'FLOAT_CONST':
            self.match('FLOAT_CONST')
            return

        if self.current.type == 'TRUE':
            self.match('TRUE')
            return

        if self.current.type == 'FALSE':
            self.match('FALSE')
            return

        if self.current.type == 'LBRACKET':
            self.match('LBRACKET')
            self.logic()
            self.match('RBRACKET')
            return

    def term_prime(self):
        if self.current.type == 'MULT':
            self.match('MULT')
            self.factor()
            self.term_prime()
        elif self.current.type == 'DIV':
            self.match('DIV')
            self.factor()
            self.term_prime()
        elif self.current.type == 'LT':
            self.match('LT')
            self.expression()
        elif self.current.type == 'GT':
            self.match('GT')
            self.expression()
        elif self.current.type == 'LTE':
            self.match('LTE')
            self.expression()
        elif self.current.type == 'GTE':
            self.match('GTE')
            self.expression()
        elif self.current.type == 'EQUAL':
            self.match('EQUAL')
            self.expression()
        elif self.current.type == 'DIFERENT':
            self.match('DIFERENT')
            self.expression()