def error_message(message):  # Main function
    message = "    SyntaxError: invalid syntax\n     " + message
    print(f"\033[31m {message}")
    exit(1)


def FalseSyntaxe(data, line, position):
    text = f"Неизвестный символ в {line} строке, на " \
           f"{position} позиции: {data}"
    return error_message(text)


def FalseKod(line):
    text = f"Неизвестная конструкция в {line} строке"
    return error_message(text)


def NotSymbol(data, line):
    text = f'Не хватает символа "{data}" в {line} строке'
    return error_message(text)


def IntInStartLine(data, line):
    text = f"Не корректное значение в начале {line} строки: {data}"
    return error_message(text)
