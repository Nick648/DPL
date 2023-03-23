# package DevProgLang/Main.py
from Lexer import *
from Parser import *
from Interpreter import *


def work_lex_out(tokens_list: list[Token]) -> None:
    line = 1
    print('Tokens:\nLine = 1:')
    for token in tokens_list:
        if token.get_number_line_token() != line:
            line = token.get_number_line_token()
            print(f"Line = {line}:")
        # print(">>>", token)
        token.to_string_token()


def main() -> None:
    # print(eval("12 + (6+2*4 / 7 -2"))
    filename = (input("Filename: ")).strip()
    # filename = "code"
    filename = openfile(filename)
    file = open(filename)
    code = file.read()  # str
    file.close()
    tokens = lexer(code)  # list of objects
    # work_lex_out(tokens)  # Out lexer

    print('Lexer Done!\n')

    parser = Parser(tokens)  # Object for parsing
    parser.parse()  # Start parsing for search nodes
    node_list = parser.get_node_list()  # List of nodes
    # parser.show_nodes()  # Out parser

    print('Parser Done!\n')

    inter = Interpreter(node_list)  # Object for execute
    inter.execute()  # Start execute
    # print(inter.linkedlist_values)  # Show all variables
    # print(inter.variables_values)  # Show all LinkedList

    print('\nInterpreter Done!\n')


if __name__ == '__main__':
    main()
