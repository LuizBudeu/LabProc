from register import Register


def precedence(operator):
    precedence_dict = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }
    return precedence_dict.get(operator, 0)


def infix_to_postfix(expression: str) -> str:
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

    return ''.join(output)


def evaluate_postfix(postfix_expression: str) -> str:
    stack = []
    for char in postfix_expression:
        if char.isdigit():
            stack.append(int(char))
        elif char in '+-*/^':
            operand2 = stack.pop()
            operand1 = stack.pop()
            if char == '+':
                stack.append(operand1 + operand2)
            elif char == '-':
                stack.append(operand1 - operand2)
            elif char == '*':
                stack.append(operand1 * operand2)
            elif char == '/':
                stack.append(operand1 / operand2)
            elif char == '^':
                stack.append(operand1 ** operand2)
    return stack.pop()


if __name__ == "__main__":
    expression = '3 + 4 * ( 2 - 1 ) / 3'
    expression = '20 * 30'
    postfix_expression = infix_to_postfix(expression)
    print("Postfix notation:", postfix_expression)

    print(evaluate_postfix(postfix_expression))

    # while len(postfix_expression) > 1:
    #     for c in postfix_expression:
    #         if c.isdigit():
    #             continue

    #         print(postfix_expression)

    #         i = postfix_expression.index(c) - 2
    #         a = int(postfix_expression[i])
    #         j = postfix_expression.index(c) - 1
    #         b = int(postfix_expression[j])

    #         match c:
    #             case '+':
    #                 result = a + b
    #             case '-':
    #                 result = a - b
    #             case '*':
    #                 result = a * b
    #             case '/':
    #                 result = a // b
    #             case _:
    #                 raise Exception(f"Unexpected Operation {c}")

    #         # Remove operand 'a'
    #         postfix_expression = postfix_expression[:i] + postfix_expression[i+1:]

    #         # Remove operand 'b'
    #         postfix_expression = postfix_expression[:j-1] + postfix_expression[j-1+1:]

    #         # Replace 'c' for result
    #         postfix_expression = list(postfix_expression)
    #         postfix_expression[i] = str(result)
    #         postfix_expression = ''.join(postfix_expression)

    #         print("final exp: " +postfix_expression)

    #         break

    # print(postfix_expression)
