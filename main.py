from src.arm_code_generator import ARMCodeGenerator
from src.lexer import Lexer
from src._parser import Parser


def main():
    with open('in.txt', 'r') as f:
        text = f.read()
        
    print(f"Expression: {text}")
        
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()

    code_generator = ARMCodeGenerator()
    
    print("Compiling...")
    
    if '/' in text:
        code_generator.reserve_registers(5)  # Reserve R0-R4 for division function
        
    code_generator.generate(ast)
    
    if '/' in text:
        for i in range(5):
            code_generator.release_register(code_generator.register_bank[i])
    
    assembly_code = code_generator.get_assembly_code()

    with open('out.s', 'w') as f:
            
        f.write(".global _start\n\n")
        
        if '/' in text:
            with open('division.s', 'r') as division_f:
                division_code = division_f.read()
                f.write(division_code)
                f.write("\n\n")
        
        f.write("_start:\n")
        f.write(assembly_code)
        f.write("\n_end:\n")
        
    print("Compilation successful!\nCheck 'out.s' for the assembly code. The final expression result is stored in R0.")
    
    
if __name__ == '__main__':
    main()