def calculate(expression):
    tokens = expression.split()
    values = []
    operators = []

    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }

    def apply_op():
        op = operators.pop()
        right = values.pop()
        left = values.pop()
        if op == '+':
            values.append(left + right)
        elif op == '-':
            values.append(left - right)
        elif op == '*':
            values.append(left * right)
        elif op == '/':
            values.append(left / right)

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            values.append(float(token))
        elif token in precedence:
            while operators and precedence.get(operators[-1], 0) >= precedence[token]:
                apply_op()
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':   
                apply_op()
            operators.pop()  # Remove '('

        i += 1

    while operators:
        apply_op()

    return values[0]


if __name__ == '__main__':
    expression = input("Enter expression: ")
    print(calculate(expression))