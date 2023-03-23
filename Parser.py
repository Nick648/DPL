from Nodes import *
from Tokens import *


def check_brackets(line: list[Token]):  # Static function - check brackets
    if len(line) < 3 and line[-1].get_type_token() != "COMMENT":
        k_line = line[-1].get_number_line_token()
        Errors.FalseKod(k_line)
    if line[-1].get_type_token() != "SEMICOLON" and line[-1].get_type_token() != "COMMENT":  # ;
        k_line = line[-1].get_number_line_token()
        Errors.NotSymbol(';', k_line)
    flag_1, flag_2, flag_3 = 0, 0, 0
    for elem in line:
        if elem.get_type_token() == "L_BRACKET" and flag_1 > -1:
            flag_1 += 1
        if elem.get_type_token() == "R_BRACKET":
            flag_1 -= 1
        if elem.get_type_token() == "L_BRACE" and flag_2 > -1:
            flag_2 += 1
        if elem.get_type_token() == "R_BRACE":
            flag_2 -= 1
        if elem.get_type_token() == "L_SQUARE_BRACKET" and flag_3 > -1:
            flag_3 += 1
        if elem.get_type_token() == "R_SQUARE_BRACKET":
            flag_3 -= 1
    if flag_1 != 0:
        Errors.NotSymbol(")", line)
    if flag_2 != 0:
        Errors.NotSymbol("}", line)
    if flag_3 != 0:
        Errors.NotSymbol("]", line)


class Parser:

    def __init__(self, tokens: list[Token]):  # Constructor
        self.kod = list()
        self.tokens = tokens
        self.node_list = list()
        self.split_on_lines()

    def split_on_lines(self) -> None:  # Division into lines of code
        pos = 0
        for i in range(len(self.tokens)):
            if self.token_type(i, "NEWLINE") or self.token_type(i, "KW_EXIT"):
                if self.tokens[pos:i]:
                    self.kod.append(self.tokens[pos:i])
                pos = i + 1
        if self.tokens[pos:]:
            self.kod.append(self.tokens[pos:])

    def token_type(self, pos: int, typ: str) -> bool:  # Token comparison
        # print(self.tokens[pos].getTypeToken(), "?", typ, "pos", pos)
        if self.tokens[pos].get_type_token() == typ:
            return True
        return False

    def parse(self) -> list[Node]:  # Main parse
        # print(self.kod, len(self.kod), len(self.kod[0]))
        for ii in range(len(self.kod)):  # Lines of code
            line = self.kod[ii]
            check_brackets(line)

            if line[0].get_type_token() == "VAR" and line[1].get_type_token() == "ASSIGN":
                self.node_list.append(self.set_assign(line))
            elif line[0].get_type_token() == "VAR" and line[1].get_type_token() == "KW_INPUT":
                self.node_list.append(self.set_input(line))
            elif line[0].get_type_token() == "COMMENT":
                continue
            elif line[0].get_type_token() == "KW_PRINT":
                self.node_list.append(self.set_print(line))
            elif line[0].get_type_token() == "KW_IF":
                self.node_list.append(self.set_if_while(line, "KW_IF"))
            elif line[0].get_type_token() == "KW_WHILE":
                self.node_list.append(self.set_if_while(line, "KW_WHILE"))
            elif line[0].get_type_token() == "KW_FOR":
                self.node_list.append(self.set_for(line))
            elif line[0].get_type_token() == "KW_LIST":
                self.node_list.append(self.set_linked_list(line))
            elif line[1].get_type_token()[:3] == "LL_":
                self.node_list.append(self.set_linked_list_operation(line, line[1].get_type_token()))
            else:
                Errors.FalseKod(ii + 1)
        # self.show_nodes()
        return self.node_list

    def set_assign(self, line: list[Token]) -> AssignNode:
        name_variable = line[0].get_value_token()
        value = line[2:len(line) - 1]
        if len(value) == 1:
            type_token = value[0].get_type_token()
            if type_token == "INT" or type_token == "VAR" or type_token == "FLOAT":
                return AssignNode(name_variable, value, type_token)
        else:
            if len(value) == 3:
                return AssignNode(name_variable, self.set_operation(value), "Operation")
            else:
                return AssignNode(name_variable, self.set_operation(value), "OperationHard")

    @staticmethod
    def set_input(line: list[Token]) -> InputNode:
        name_variable = line[0].get_value_token()
        flag = 1
        com = list()
        for elem in line:
            if flag == 1 and elem.get_value_token() == "'":
                flag = 2
            elif flag == 2:
                if elem.get_value_token() == "'":
                    break
                com.append(elem)
        if len(com) == 0:
            return InputNode(name_variable, None)
        else:
            comment = ''
            for i in com:
                comment += i.get_value_token() + ' '
            return InputNode(name_variable, comment)

    @staticmethod
    def set_print(line: list[Token]) -> PrintNode:
        # value = line[1:len(line) - 1]
        value = line[2:len(line) - 2]
        if len(value) == 1:
            type_value = value[0].get_type_token()
            if type_value == "INT" or type_value == "FLOAT":
                return PrintNode(value, type_value)
            elif type_value == "VAR":
                return PrintNode(value, type_value)
            else:
                Errors.FalseKod(line[0].get_number_line_token())
        else:
            vars_list = list()
            for pos_i in range(len(value)):
                type_value = value[pos_i].get_type_token()
                if type_value == "INT" or type_value == "FLOAT" or type_value == "VAR":
                    vars_list.append(value[pos_i])
                elif type_value == "COMMA":
                    continue
                else:
                    Errors.FalseKod(line[0].get_number_line_token())
            return PrintNode(vars_list, "ListVars")

    def set_if_while(self, line: list[Token], key_word: str) -> Node:
        num_line = line[0].get_number_line_token()
        flag = 1
        condition = list()
        loop = list()
        line_kod = list()
        for elem in line:
            if flag == 1 and elem.get_value_token() == "(":
                flag = 2
            elif flag == 2:
                if elem.get_value_token() == ")":
                    flag = 3
                    continue
                condition.append(elem)
            elif flag == 3 and elem.get_value_token() == "{":
                flag = 4
            elif flag == 4:
                if elem.get_value_token() == "}":
                    flag = 5
                    continue
                line_kod.append(elem)
                if elem.get_value_token() == ";":
                    loop.append(line_kod)
                    line_kod = list()
        ready_loop = list()
        for line in loop:
            if line[0].get_type_token() == "VAR" and line[1].get_type_token() == "ASSIGN":
                ready_loop.append(self.set_assign(line))
            elif line[0].get_type_token() == "KW_PRINT":
                ready_loop.append(self.set_print(line))
            else:
                Errors.FalseKod(num_line)
        # print(f'{key_word}:')
        # print("Condition:", [elem.getValue() for elem in condition])
        # print("Ready_loop:", [elem.getTypeNode() for elem in ready_loop])
        if key_word == "KW_IF":
            return IfNode(condition, ready_loop)
        elif key_word == "KW_WHILE":
            return WhileNode(condition, ready_loop)

    def set_for(self, line: list[Token]) -> ForNode:
        num_line = line[0].get_number_line_token()
        flag = 1
        condition = list()
        loop = list()
        line_kod = list()
        name_var = ''
        if len(line) > 10:
            fr, name_var, inn = line[0].get_type_token(), line[1].get_type_token(), line[2].get_type_token()
            if fr == 'KW_FOR' and name_var == 'VAR' and inn == 'KW_IN':
                name_var = line[1].get_value_token()
            else:
                Errors.FalseKod(num_line)
        else:
            Errors.FalseKod(num_line)

        for elem in line:
            if flag == 1 and elem.get_value_token() == "(":
                flag = 2
            elif flag == 2:
                if elem.get_value_token() == ")":
                    flag = 3
                    continue
                condition.append(elem)
            elif flag == 3 and elem.get_value_token() == "{":
                flag = 4
            elif flag == 4:
                if elem.get_value_token() == "}":
                    flag = 5
                    continue
                line_kod.append(elem)
                if elem.get_value_token() == ";":
                    loop.append(line_kod)
                    line_kod = list()
        ready_loop = list()
        for line in loop:
            if line[0].get_type_token() == "VAR" and line[1].get_type_token() == "ASSIGN":
                ready_loop.append(self.set_assign(line))
            elif line[0].get_type_token() == "KW_PRINT":
                ready_loop.append(self.set_print(line))
            else:
                Errors.FalseKod(num_line)
        # print("Condition:", [elem.getValue() for elem in condition])
        # print("Ready_loop:", [elem.getTypeNode() for elem in ready_loop])
        if len(condition) == 3 and condition[1].get_type_token() == 'COMMA':
            if condition[0].get_type_token() == 'INT' or condition[0].get_type_token() == 'VAR' \
                    and condition[2].get_type_token() == 'INT' or condition[2].get_type_token() == 'VAR':
                return ForNode(name_var, condition, ready_loop)
        Errors.FalseKod(num_line)

    @staticmethod
    def set_operation(value: list[Token]) -> OperationNode:
        if len(value) == 3:
            left_operand = value[0]
            sign = value[1]
            right_operand = value[2]
            return OperationNode(left_operand, right_operand, sign, final=True)
        else:
            # condition = [elem.getValue() for elem in value]
            # print(condition)
            return OperationNode(value, None, None, final=False)

    @staticmethod
    def set_linked_list(line: list[Token]) -> LinkedListNode:
        name_linked_list = line[1].get_value_token()
        values = line[4:len(line) - 2]
        new_values = list()
        for elem in values:
            if elem.get_type_token() != "COMMA":
                new_values.append(elem)
        return LinkedListNode(name_linked_list, new_values)

    @staticmethod
    def set_linked_list_operation(line: list[Token], token_type: str) -> LinkedListOperationNode:
        name_variable = line[0].get_value_token()
        flag, value = 1, -1
        digits = list()
        for elem in line:
            if flag == 1 and elem.get_value_token() == "(":
                flag = 2
            elif flag == 2:
                if elem.get_value_token() == ")":
                    break
                digits.append(elem)
        if len(digits) == 1 and digits[0].get_type_token() == 'INT':
            value = digits[0]
        if len(digits) == 0:
            value = ""

        if token_type == 'LL_INSERT_END' and value != -1 and value != "":
            return LinkedListOperationNode("setLLInsertAtEnd", name_variable, value)
        elif token_type == 'LL_INSERT_HEAD' and value != -1 and value != "":
            return LinkedListOperationNode("setLLInsertAtHead", name_variable, value)
        elif token_type == 'LL_DELETE' and value != -1:
            return LinkedListOperationNode("setLLDelete", name_variable, value)
        elif token_type == 'LL_DELETE_HEAD':
            return LinkedListOperationNode("setLLDeleteAtHead", name_variable, None)
        elif token_type == 'LL_SEARCH' and value != -1 and value != "":
            return LinkedListOperationNode("setLLSearch", name_variable, value)
        elif token_type == 'LL_IS_EMPTY':
            return LinkedListOperationNode("setLLIsEmpty", name_variable, None)
        elif token_type == 'LL_LEN':
            return LinkedListOperationNode("setLLLen", name_variable, None)
        else:
            Errors.FalseKod(line[0].get_number_line_token())

    def get_node_list(self) -> list[Node]:
        return self.node_list

    def show_nodes(self) -> None:
        print("\tself.node_list:")
        for elem in self.node_list:
            print(elem.get_type_node())
