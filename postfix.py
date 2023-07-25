def precedence(operator):
    precedence_dict = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }
    return precedence_dict.get(operator, 0)


def infix_to_postfix(expression):
    output = []
    operator_stack = []

    for char in expression:
        if char.isdigit() or char.isalpha():
            output.append(char)
        elif char in '+-*/^':
            while (operator_stack and
                   operator_stack[-1] in '+-*/^' and
                   precedence(operator_stack[-1]) >= precedence(char)):
                output.append(operator_stack.pop())
            operator_stack.append(char)
        elif char == '(':
            operator_stack.append(char)
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()

    while operator_stack:
        output.append(operator_stack.pop())

    return output


if __name__ == "__main__":
    expression = '3 + 4 * ( 2 - 1 ) / 3'
    postfix_expression = infix_to_postfix(expression)
    print("Postfix notation:", ''.join(postfix_expression))
