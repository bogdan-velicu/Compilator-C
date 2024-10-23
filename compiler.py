# Define token types
keywords = {"int", "string", "if", "else", "return", "scanf", "printf", "float"}
operators = {"+", "++", "-", "--", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!", "&"}
separators = {"(", ")", "{", "}", ",", ";", "[", "]"}

def skip_whitespace_and_newlines(file_content, pointer, current_line):
    while pointer < len(file_content) and file_content[pointer] in {' ', '\t', '\n'}:
        if file_content[pointer] == '\n':
            current_line += 1
        pointer += 1
    return pointer, current_line

def handle_preprocessor_directive(file_content, pointer, current_line):
    start_pointer = pointer
    pointer += 1
    while pointer < len(file_content) and file_content[pointer] != '\n':
        pointer += 1
    token = file_content[start_pointer:pointer]
    return token, pointer, current_line

def handle_identifier_or_keyword(file_content, pointer):
    start_pointer = pointer
    while pointer < len(file_content) and (file_content[pointer].isalnum() or file_content[pointer] == '_'):
        pointer += 1
    token = file_content[start_pointer:pointer]
    token_type = "keyword" if token in keywords else "identifier"
    return token, token_type, pointer

def handle_number(file_content, pointer):
    start_pointer = pointer
    while pointer < len(file_content) and file_content[pointer].isdigit():
        pointer += 1
    if pointer < len(file_content) and file_content[pointer] == '.':
        pointer += 1
        while pointer < len(file_content) and file_content[pointer].isdigit():
            pointer += 1
    token = file_content[start_pointer:pointer]
    return token, pointer

def handle_string(file_content, pointer, current_line):
    start_line = current_line
    pointer += 1
    start_pointer = pointer
    while pointer < len(file_content) and file_content[pointer] != '"':
        if file_content[pointer] == '\\':
            if pointer + 1 < len(file_content) and file_content[pointer + 1] == '\n':
                current_line += 1
                pointer += 2
            else:
                pointer += 2
        else:
            if file_content[pointer] == '\n':
                current_line += 1
            pointer += 1
    token = file_content[start_pointer:pointer]
    pointer += 1
    return token, start_line, pointer, current_line

def handle_single_line_comment(file_content, pointer):
    start_pointer = pointer
    pointer += 2
    while pointer < len(file_content) and file_content[pointer] != '\n':
        pointer += 1
    token = file_content[start_pointer:pointer].strip()
    return token, pointer

def handle_multi_line_comment(file_content, pointer, current_line):
    pointer += 2
    start_pointer = pointer
    start_line = current_line
    while pointer + 1 < len(file_content) and (file_content[pointer] != '*' or file_content[pointer + 1] != '/'):
        if file_content[pointer] == '\n':
            current_line += 1
        pointer += 1
    pointer += 2
    comment_text = file_content[start_pointer:pointer-2]
    return comment_text, start_line, pointer, current_line

def handle_operator(file_content, pointer):
    start_pointer = pointer
    if pointer + 1 < len(file_content) and file_content[pointer:pointer + 2] in operators:
        token = file_content[pointer:pointer + 2]
        pointer += 2
    else:
        token = file_content[pointer]
        pointer += 1
    return token, pointer

def handle_separator(file_content, pointer):
    token = file_content[pointer]
    pointer += 1
    return token, pointer

def tokenize(file_content):
    pointer = 0
    current_line = 1
    tokens = []

    while pointer < len(file_content):
        pointer, current_line = skip_whitespace_and_newlines(file_content, pointer, current_line)
        if pointer >= len(file_content):
            break

        start_pointer = pointer

        if file_content[pointer] == '#':
            token, pointer, current_line = handle_preprocessor_directive(file_content, pointer, current_line)
            tokens.append((token, current_line, "preprocessor directive", pointer - start_pointer, start_pointer))

        elif file_content[pointer].isalpha() or file_content[pointer] == '_':
            token, token_type, pointer = handle_identifier_or_keyword(file_content, pointer)
            tokens.append((token, current_line, token_type, pointer - start_pointer, start_pointer))

        elif file_content[pointer].isdigit():
            token, pointer = handle_number(file_content, pointer)
            tokens.append((token, current_line, "number", pointer - start_pointer, start_pointer))

        elif file_content[pointer] == '"':
            token, start_line, pointer, current_line = handle_string(file_content, pointer, current_line)
            tokens.append((token, start_line, "string", pointer - start_pointer, start_pointer))

        elif file_content[pointer] == '/' and pointer + 1 < len(file_content) and file_content[pointer + 1] == '/':
            token, pointer = handle_single_line_comment(file_content, pointer)
            tokens.append((token, current_line, "comment", pointer - start_pointer, start_pointer))

        elif file_content[pointer] == '/' and pointer + 1 < len(file_content) and file_content[pointer + 1] == '*':
            token, start_line, pointer, current_line = handle_multi_line_comment(file_content, pointer, current_line)
            tokens.append((token, start_line, "comment", len(token), start_pointer))

        elif file_content[pointer] in operators:
            token, pointer = handle_operator(file_content, pointer)
            tokens.append((token, current_line, "operator", len(token), start_pointer))

        elif file_content[pointer] in separators:
            token, pointer = handle_separator(file_content, pointer)
            tokens.append((token, current_line, "separator", 1, start_pointer))

        else:
            token = file_content[pointer]
            print(f'Eroare lexicală la linia {current_line}, caracter necunoscut: "{token}" la poziția {start_pointer}')
            tokens.append((token, current_line, "lexical error", 1, start_pointer))
            pointer += 1

    return tokens

def analyze_file(file_name):
    with open(file_name, 'r') as f:
        file_content = f.read()

    tokens = tokenize(file_content)

    for token, line, token_type, length, start_pointer in tokens:
        print(f'Token: "{token}" | Line: {line} | Type: {token_type} | Length: {length}')

if __name__ == "__main__":
    analyze_file("exemplu.c")