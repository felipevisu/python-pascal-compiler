class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = tokens[0]
        self.index = 0
        self.size = len(tokens)

    def parse(self):
        self.program()

    def match(self, token):
        if self.current.type == token:
            self.index += 1
            if self.index < self.size:
                self.current = self.tokens[self.index]
        else:
            print('Deu erro')
            
    def program(self):
        print('program', self.current.type)
        if self.current.type == 'PROGRAM':
            self.match('PROGRAM')
            self.match('ID')
            self.match('PCOMMA')
            self.declarations()

    def declarations(self):
        print('declarations', self.current.type)
        self.var_decl()
        return

    def var_decl(self):
        print('var_decl', self.current.type)
        if self.current.type == 'VAR':
            self.match('VAR')
        else:
            self.begin()
            return

        while True:
            if self.current.type == 'ID':
                self.match('ID')
            if self.current.type == 'COMMA':
                self.match('COMMA')
            if self.current.type == 'TWOPOINT':
                self.match('TWOPOINT')
                break

        if self.current.type == 'REAL':
            self.match('REAL')

        if self.current.type == 'INTEGER':
            self.match('INTEGER')

        if self.current.type == 'STRING':
            self.match('STRING')

        if self.current.type == 'BOOLEAN':
            self.match('BOOLEAN')

        if self.current.type == 'PCOMMA':
            self.match('PCOMMA')

        self.var_decl()

    def begin(self):
        print('begin', self.current.type)
        if self.current.type == 'BEGIN':
            self.match('BEGIN')

            while self.current.type != 'END':
                self.statements()

            if self.current.type == 'END':
                print('Compilado')

    def statements(self):
        print('statements', self.current.type)
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

        return

    def for_statement(self):
        print('for_statement', self.current.type)
        self.match('FOR')
        self.statements()
        self.match('TO')
        self.factor()
        self.match('DO')
        self.statements()

    def while_statement(self):
        print('while_statement', self.current.type)
        self.match('WHILE')
        self.logic()
        self.match('DO')
        self.statements()
        return

    def if_statement(self):
        print('if_statement', self.current.type)
        self.match('IF')
        self.logic()
        self.match('THEN')
        self.statements()

        if self.current.type == 'ELSE':
            self.match('ELSE')
            self.statements()

    def print(self):
        self.match('PRINT')
        self.match('LBRACKET')
        self.logic()
        self.match('RBRACKET')
        self.match('PCOMMA')

    def read(self):
        self.match('READ')
        self.match('ID')
        self.match('PCOMMA')

    def logic(self):
        print('logic', self.current.type)
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
        print('expression', self.current.type)
        self.term()
        self.expression_prime()
    
    def term(self):
        print('term', self.current.type)
        self.factor()
        self.term_prime()

    def expression_prime(self):
        print('expression_prime', self.current.type)
        if self.current.type == 'PLUS':
            self.match('PLUS')
            self.term()
            self.expression_prime()
        elif self.current.type == 'MINUS':
            self.match('MINUS')
            self.term()
            self.expression_prime()
        else:
            pass

    def factor(self):
        print('factor', self.current.type)
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
        print('term_prime', self.current.type)
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
        else:
            pass