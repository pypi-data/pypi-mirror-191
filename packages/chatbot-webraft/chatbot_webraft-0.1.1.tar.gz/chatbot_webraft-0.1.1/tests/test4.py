import ast

def generate_code(text):
    try:
        tree = ast.parse(text)
        code = compile(tree, filename="<string>", mode="exec")
        return code
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        return None

def execute_code(code):
    try:
        exec(code)
    except Exception as e:
        print(f"Execution error: {e}")

def main():
    text = input("Enter code: ")
    code = generate_code(text)
    if code:
        print(code)
        execute_code(code)

if __name__ == '__main__':
    main()
