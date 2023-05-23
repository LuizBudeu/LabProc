from __future__ import annotations
from token1 import Token, TokenType
from lexer import Lexer


class InvalidSyntax(Exception):
    pass


class AST:
    @staticmethod
    def print_ast(node, level: int = 0) -> None:
        indent = '  ' * level
        if isinstance(node, BinOp):
            print(f'{indent}BinOp({node.op.type})')
            AST.print_ast(node.left, level + 1)
            AST.print_ast(node.right, level + 1)
        elif isinstance(node, Num):
            print(f'{indent}Num({node.value})')


class Num(AST):
    def __init__(self, value: int) -> None:
        self.value = value


class BinOp(AST):
    def __init__(self, left: Branch, op: Token, right: Branch) -> None:
        self.left = left
        self.op = op
        self.right = right


Branch = AST | BinOp | Num | None


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self) -> None:
        raise InvalidSyntax(f'Invalid syntax at position {self.lexer.pos}')

    def eat(self, token_type: TokenType) -> None:
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self) -> Branch:
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(int(token.value)) 
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

    def term(self) -> Branch:
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self) -> Branch:
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self) -> Branch:
        return self.expr()
    
    
if __name__ == '__main__':
    text = '3 + 4 * (10 - 5 / (1*2 - 4))'
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()

    AST.print_ast(ast)


