def generate_pycode(text):
    lines = text.strip().split("\n")
    code = ""
    indent_level = 0
    for line in lines:
        if "print" in line:
            # generate print statement
            code += " " * 4 * indent_level + "print(" + line.split("print")[1].strip() + ")\n"
        elif "define" in line:
            # generate variable definition
            parts = line.split("define")[1].strip().split("as")
            variable_name = parts[0].strip()
            variable_value = parts[1].strip()
            code += f"{' ' * 4 * indent_level}{variable_name} = {variable_value}\n"
        elif "if" in line:
            # generate if statement
            code += f"{' ' * 4 * indent_level}if {line.split('if')[1].strip()}:\n"
            indent_level += 1
        elif "else" in line:
            # generate else statement
            indent_level -= 1
            code += f"{' ' * 4 * indent_level}else:\n"
            indent_level += 1
        elif "elif" in line:
            # generate elif statement
            indent_level -= 1
            code += f"{' ' * 4 * indent_level}elif {line.split('elif')[1].strip()}:\n"
            indent_level += 1
        elif "end" in line:
            # end if/else statement
            indent_level -= 1
        elif "for" in line:
            # generate for loop
            code += f"{' ' * 4 * indent_level}for {line.split('for')[1].strip()}:\n"
            indent_level += 1
        elif "while" in line:
            # generate while loop
            code += f"{' ' * 4 * indent_level}while {line.split('while')[1].strip()}:\n"
            indent_level += 1
        elif "break" in line:
            # generate break statement
            code += f"{' ' * 4 * indent_level}break\n"
        elif "continue" in line:
            # generate continue statement
            code += f"{' ' * 4 * indent_level}continue\n"
        elif "pass" in line:
            # generate pass statement
            code += f"{' ' * 4 * indent_level}pass\n"
        elif "function" in line:
            # generate function definition
            parts = line.split("function")[1].strip().split("(")
            function_name = parts[0].strip()
            arguments = parts[1].strip().split(")")[0]
            code += f"{' ' * 4 * indent_level}def {function_name}({arguments}):\n"
            indent_level += 1
        elif "return" in line:
            # generate return statement
            code += f"{' ' * 4 * indent_level}return {line.split('return')[1].strip()}\n"
        else:
            code += "Unrecognized command."
        return code

def codewriter(language,text,model):
    if language=="python":
        code = generate_pycode(text)
        return code
    else:
        return "Language not supported"
