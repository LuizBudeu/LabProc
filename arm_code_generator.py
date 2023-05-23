from lexer import Lexer
from token1 import TokenType
from parser1 import Parser, Num, BinOp, Branch
from register import Register, RegisterDoesntExist, NoRegistersAvailable


MAX_REGISTER_COUNT = 15


class ARMCodeGenerator:
    def __init__(self) -> None:
        self.register_bank = [Register(i) for i in range(MAX_REGISTER_COUNT)]
        self.result = ""

    def get_register(self , register_id: int | None = None) -> Register:
        if register_id is not None:
            try:
                register = self.register_bank[register_id]
            except IndexError:
                raise RegisterDoesntExist(f"Register {register_id} doesn't exist")
            
            register.in_use = True
            
        else:
            for register in self.register_bank:
                if not register.in_use:
                    register.in_use = True
                    break
            else:
                raise NoRegistersAvailable("No registers available")
            
        return register

    def release_register(self, register: Register) -> None:
        register.in_use = False

    def generate(self, node: Branch) -> Register:
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

            self.release_register(left_register)  # Release registers used by children
            self.release_register(right_register)

            return result_register
        
        else:
            raise TypeError(f"Invalid node type: {type(node)}")

    def get_assembly_code(self) -> str:
        return self.result


text = '(3 + 4 * (10 - 5) + 1)'  # 240
lexer = Lexer(text)
parser = Parser(lexer)
ast = parser.parse()

code_generator = ARMCodeGenerator()
code_generator.generate(ast)
assembly_code = code_generator.get_assembly_code()

print(assembly_code)
