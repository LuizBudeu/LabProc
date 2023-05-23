from lexer import Lexer
from token1 import TokenType
from parser1 import Parser, Num, BinOp, Branch


class ARMCodeGenerator:
    def __init__(self):
        self.register_count = 0
        self.result = ""

    def get_register(self):
        register = f"r{self.register_count}"
        self.register_count += 1
        return register

    def release_register(self):
        self.register_count -= 1

    def generate(self, node: Branch):
        if isinstance(node, Num):
            register = self.get_register()
            self.result += f"    MOV {register}, #{node.value}\n"
            return register
        elif isinstance(node, BinOp):
            left_register = self.generate(node.left)
            right_register = self.generate(node.right)
            result_register = self.get_register()

            if node.op.type == TokenType.PLUS:
                self.result += f"    ADD {result_register}, {left_register}, {right_register}\n"
            elif node.op.type == TokenType.MINUS:
                self.result += f"    SUB {result_register}, {left_register}, {right_register}\n"
            elif node.op.type == TokenType.MULTIPLY:
                self.result += f"    MUL {result_register}, {left_register}, {right_register}\n"
            elif node.op.type == TokenType.DIVIDE:
                self.result += f"    SDIV {result_register}, {left_register}, {right_register}\n"

            self.release_register()  # Release registers used by children
            self.release_register()

            return result_register

    def get_assembly_code(self):
        return self.result


text = '(3 + 4 * (10 - 5) + 1) * 8 * (2 + 3)'
lexer = Lexer(text)
parser = Parser(lexer)
ast = parser.parse()

code_generator = ARMCodeGenerator()
code_generator.generate(ast)
assembly_code = code_generator.get_assembly_code()

print(assembly_code)