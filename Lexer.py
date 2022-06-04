# package DevProgLang/Lexer.py
import Errors
import sys
import re
import os
from Tokens import *


def lexer(characters):  # lexer
    position, line = 0, 1
    pos = 0  # for re
    tokens = []
    while pos < len(characters):
        # print("pos", ">" * 10, pos)
        match = None
        for token_exp in token_exprs:  # token_expression from Tokens.py
            pattern, tag = token_exp
            regex = re.compile(pattern)  # use reg
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = Token(tag, text, line, position)  # Object
                    # token = (text, tag)  # Tokens: [('5', 'INT'), ('+', 'PLUS_OP'),...
                    tokens.append(token)
                    position += 1
                    if tag == 'NEWLINE':
                        line += 1
                        position = 0
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            Errors.FalseSyntaxe(characters[pos], line, position)
            # sys.exit(1)
        else:
            pos = match.end(0)  # new pos
    return tokens


# Is the file open?
def openfile(filename):
    if ".txt" not in filename:
        filename += ".txt"
    filename = os.path.abspath('venv/data') + '/' + filename
    # filename = 'data/' + filename
    # print(f'Current Working Directory is: {os.getcwd()}')
    # print('filename:', filename)
    try:
        with open(file=filename, mode='r', encoding='utf-8') as _:
            print('\nEverything is OK! The file is open!\n')
            return filename
    except FileNotFoundError:  # Error
        message = "\n    You DON'T have a file with that name!"
        print(f"\033[31m {message}")
        exit(1)
