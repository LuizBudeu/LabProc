from __future__ import annotations
from ._token import Token, TokenType
from .lexer import Lexer


class InvalidSyntax(Exception):
    pass


class AST:

    @staticmethod
    def _print_ast(node: Node, level: int = 0) -> str:
        # indent = '  ' * level
        # if isinstance(node, BinOp):
        #     print(f'{indent}BinOp({node.op.type})')
        #     AST.print_ast(node.left, level + 1)
        #     AST.print_ast(node.right, level + 1)
        # elif isinstance(node, Num):
        #     print(f'{indent}Num({node.value})')

        indent = '  ' * level
        if isinstance(node, BinOp):
            left_str = AST._print_ast(node.left, level + 1)
            right_str = AST._print_ast(node.right, level + 1)
            return f'{indent}BinOp({node.op.type})\n{left_str}\n{right_str}'

        elif isinstance(node, Num):
            return f'{indent}Num({node.value})'

        else:
            return f'{indent}Unknown'

    def __str__(self) -> str:
        return AST._print_ast(self)


class Num(AST):
    def __init__(self, value: int) -> None:
        self.value = value

    # def __str__(self) -> str:
    #     return f'{self.value}'

    def as_string(self):
        return str(self.value)


class BinOp(AST):
    def __init__(self, left: Node, op: Token, right: Node) -> None:
        self.left = left
        self.op = op
        self.right = right

    # def __str__(self) -> str:
    #     return f'({self.left} {self.op.type} {self.right})'

    def as_string(self):
        return self.op.value


Node = AST | BinOp | Num | None


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

    def factor(self) -> Node:
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(int(token.value))
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

    def term(self) -> Node:
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self) -> Node:
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self) -> Node:
        return self.expr()


if __name__ == '__main__':
    text = '3 + 4 * (10 - 5 / (1*2 - 4))'
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()

    print(ast)

    print()

    # def operation_order(ast):
    #     def dfs_reverse(node, result_list, indent_level):
    #         if isinstance(node, Num):
    #             result_list.append((indent_level, node.value))
    #         elif isinstance(node, BinOp):
    #             dfs_reverse(node.right, result_list, indent_level + 1)
    #             result_list.append((indent_level, node.op))
    #             dfs_reverse(node.left, result_list, indent_level + 1)

    #     ordered_list = []
    #     dfs_reverse(ast, ordered_list, 0)
    #     return [value for _, value in ordered_list]

    # ordered_list = operation_order(ast)
    # print(ordered_list)
    print()
