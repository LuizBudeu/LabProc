from .lexer import Lexer
from ._token import TokenType
from ._parser import Parser, Num, BinOp, Node, AST
from .register import Register, RegisterDoesntExist, NoRegistersAvailable


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
                raise RegisterDoesntExist(f"Register {register_id} doesn't exist")

            register.in_use = True

        else:
            for register in self.register_bank:
                if not register.in_use:
                    register.in_use = True
                    break
            else:
                raise NoRegistersAvailable(f"All {MAX_REGISTER_COUNT} registers are in use")

        return register
    
    def get_final_register(self) -> Register:
        for register in self.register_bank:
            if register.in_use:
                return register
        else:
            raise Exception(f"Can't find final register")

    def release_register(self, register: Register) -> None:
        register.in_use = False
        
    def reserve_registers(self, count: int) -> list[Register]:
        reserved_registers = []
        for register in self.register_bank:
            if not register.in_use:
                reserved_registers.append(register)
                register.in_use = True
                if len(reserved_registers) == count:
                    return reserved_registers
                
        raise Exception("Not enough available registers for reservation")

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
                self.result += f"    MOV r1, {left_register}  ;@ dividendo\n"
                self.result += f"    MOV r0, {right_register}  ;@ divisor\n"
                self.result += f"    bl _divide\n"
                self.result += f"    MOV {result_register}, r3  ;@ resultado\n"
                
                # Reset registers used by division
                for i in range(4):
                    reg = self.register_bank[i]
                    reg.content = 0  
                
                result_register.content = left_register.content // right_register.content

            # Release registers used by children
            self.release_register(left_register)
            self.release_register(right_register)

            return result_register

        else:
            raise TypeError(f"Invalid node type: {type(node)}")

    def get_assembly_code(self) -> str:
        result_register = self.get_final_register()
        self.result += f"    MOV r0, {result_register}\n"
        return self.result


if __name__ == "__main__":
    # text = '(3 + 4 * (10 - 5) + 1) * (10 - 3)'  # 168
    text = '(1 - 4 / 2) - 10 / 2 '  # -6
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()

    code_generator = ARMCodeGenerator()
    
    if '/' in text:
        code_generator.reserve_registers(5)  # Reserve R0-R4 for division function
        
    code_generator.generate(ast)
    
    if '/' in text:
        for i in range(5):
            code_generator.release_register(code_generator.register_bank[i])
    
    assembly_code = code_generator.get_assembly_code()

    print(assembly_code)
