import re

class Parser:
    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            self.tokens = self.tokenize(f.read())
            print(self.tokens)
        self.pos = 0

    def tokenize(self, input_str):
        token_specification = [
            ('IF', r'if'),
            ('ELSE', r'else'),
            ('WHILE', r'while'),
            ('ID', r'[A-Za-z]+'),
            ('INT_LIT', r'\d+'),
            ('FLOAT_LIT', r'\d+\.\d+'),
            ('OP', r'[+\-*/%]'),
            ('BOOL_OP', r'[><=!&|]+'),
            ('LPAR', r'\('),
            ('RPAR', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('SEMI', r';')
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        return [match.lastgroup for match in re.finditer(tok_regex, input_str)]

    def match(self, token_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == token_type:
            self.pos += 1
            return True
        return False

    def stmt(self):
        return self.if_stmt() or self.block() or self.expr() or self.while_loop()

    def stmt_list(self):
        while self.stmt():
            if not self.match('SEMI'):
                return False
        return True

    def while_loop(self):
        if not self.match('WHILE'):
            return False
        if not self.match('LPAR'):
            return False
        if not self.bool_expr():
            return False
        if not self.match('RPAR'):
            return False
        if not (self.stmt() and self.match('SEMI')) and not self.block():
            return False
        return True

    def if_stmt(self):
        if not self.match('IF'):
            return False
        if not self.match('LPAR'):
            return False
        if not self.bool_expr():
            return False
        if not self.match('RPAR'):
            return False
        if not (self.stmt() and self.match('SEMI')) and not self.block():
            return False
        if self.match('ELSE'):
            if not (self.stmt() and self.match('SEMI')) and not self.block():
                return False
        return True

    def block(self):
        if not self.match('LBRACE'):
            return False
        if not self.stmt_list():
            return False
        if not self.match('RBRACE'):
            return False
        return True

    def expr(self):
        if not self.term():
            return False
        while self.match('OP'):
            if not self.term():
                return False
        return True

    def term(self):
        if not self.fact():
            return False
        while self.match('OP'):
            if not self.fact():
                return False
        return True

    def fact(self):
        if (self.match('ID') or
                self.match('INT_LIT') or
                self.match('FLOAT_LIT')):
            return True
        elif (self.match('LPAR') and
              self.expr() and
              self.match('RPAR')):
            return True
        else:
            return False

    def bool_expr(self):
        if not self.bterm():
            return False
        while self.match('BOOL_OP'):
            if not self.bterm():
                return False
        return True

    def bterm(self):
        if not self.band():
            return False
        while self.match('BOOL_OP'):
            if not self.band():
                return False
        return True

    def band(self):
        if not self.bor():
            return False
        while self.match('BOOL_OP'):
            if not self.bor():
                return False
        return True

    def bor(self):
        if not self.expr():
            return False
        while self.match('BOOL_OP'):
            if not self.expr():
                return False
        return True


parser = Parser('input.txt')
if parser.stmt():
    print('The token list is in the language.')
else:
    print('The token list is not in the language.')