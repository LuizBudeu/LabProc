from _token import Token, TokenType


class InvalidCharacterException(Exception):
    pass


class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self) -> None:
        raise InvalidCharacterException(f"Invalid character '{self.current_char}' at position {self.pos}")

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self) -> int:
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self) -> Token:
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            self.error()

        return Token(TokenType.EOF, '')



if __name__ == '__main__':
    text = '3 + 4 * (10 - 5) / 4 * (-1)    '
    lexer = Lexer(text)

    while True:
        token = lexer.get_next_token()
        if token.type == TokenType.EOF:
            break
        print(token)
