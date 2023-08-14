from enum import Enum


class TokenType(Enum):
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    EOF = 'EOF'


class Token:
    def __init__(self, type: TokenType, value: str | int):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

