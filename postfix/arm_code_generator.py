from lexer import Lexer
from _token import TokenType
from _parser import Parser, Num, BinOp, Node, AST
from register import Register, RegisterDoesntExist, NoRegistersAvailable


MAX_REGISTER_COUNT = 15


class ARMCodeGenerator:
    def __init__(self) -> None:
        self.register_bank = [Register(i) for i in range(MAX_REGISTER_COUNT)]
        self.result = ""

    def get_register(self, register_id: int | None = None) -> Register:
        if register_id is not None:
            try:
                register = self.register_bank[register_id]
            except IndexError:
                raise RegisterDoesntExist(
                    f"Register {register_id} doesn't exist")

            register.in_use = True

        else:
            for register in self.register_bank:
                if not register.in_use:
                    register.in_use = True
                    break
            else:
                raise NoRegistersAvailable(
                    f"All {MAX_REGISTER_COUNT} registers are in use")

        return register

    def release_register(self, register: Register) -> None:
        register.in_use = False

    def generate(self, node: Node) -> Register:
        if isinstance(node, Num):
            register = self.get_register()
            self.result += f"    MOV {register}, #{node.value}\n"
            register.content = node.value
            return register

        elif isinstance(node, BinOp):
            left_register = self.generate(node.left)
            right_register = self.generate(node.right)
            result_register = self.get_register()

            if node.op.type == TokenType.PLUS:
                self.result += f"    ADD {result_register}, {left_register}, {right_register}\n"
                result_register.content = left_register.content + right_register.content
            elif node.op.type == TokenType.MINUS:
                self.result += f"    SUB {result_register}, {left_register}, {right_register}\n"
                result_register.content = left_register.content - right_register.content
            elif node.op.type == TokenType.MULTIPLY:
                self.result += f"    MUL {result_register}, {left_register}, {right_register}\n"
                result_register.content = left_register.content * right_register.content
            elif node.op.type == TokenType.DIVIDE:
                self.result += f"    SDIV {result_register}, {left_register}, {right_register}\n"
                result_register.content = left_register.content // right_register.content

            # Release registers used by children
            self.release_register(left_register)
            self.release_register(right_register)

            return result_register

        else:
            raise TypeError(f"Invalid node type: {type(node)}")

    def get_assembly_code(self) -> str:
        return self.result


if __name__ == "__main__":
    text = '(3 + 4 * (10 - 5) + 1) * (10 - 3)'  # 168
    text2 = '3 - 5'
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()

    print(ast)
    print()

    code_generator = ARMCodeGenerator()
    code_generator.generate(ast)
    assembly_code = code_generator.get_assembly_code()

    print(assembly_code)
