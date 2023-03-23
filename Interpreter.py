from LinkList import *
from Nodes import *


class Interpreter:

    def __init__(self, node_list):
        self.node_list = node_list
        self.variables_values = dict()
        self.linkedlist_values = dict()

    def execute(self):  # Begin
        for node_item in self.node_list:
            node_type = node_item.get_type_node()
            # print("node_type:", node_type)
            if node_type == "Print":
                self.execute_print(node_item)
            elif node_type == "Input":
                self.execute_input(node_item)
            elif node_type == "If":
                self.execute_if(node_item)
            elif node_type == "While":
                self.execute_while(node_item)
            elif node_type == "For":
                self.execute_for(node_item)
            elif node_type == "Assign":
                self.execute_assign(node_item)
            elif node_type == "LinkedList":
                self.execute_linked_list(node_item)
            elif node_type == "LinkedListOperationNode":
                self.execute_linked_list_operation(node_item)
            else:
                print("ERROR(STRANGE)")

    def get_value_var(self, pos: str):
        try:
            result = self.variables_values[pos]
            return result
        except:
            Errors.error_message(f'Value of variable not found: {pos}')

    def execute_assign(self, node_item: AssignNode):
        name_variable = node_item.get_name_variable()
        type_value = node_item.get_type_value()
        # print(name_variable, type_value)

        if type_value == "INT":
            value = node_item.get_value()[0].get_value_token()
            # print(name_variable, value, node.getValue(), node.getValue()[0], node.getValue()[0].getValue())
            self.variables_values[name_variable] = value
        elif type_value == "VAR":
            # print(value)
            value = node_item.get_value()[0].get_value_token()
            self.variables_values[name_variable] = self.get_value_var(value)
        elif type_value == "Operation":
            value = self.execute_operation(node_item.get_value())
            self.variables_values[name_variable] = value
        elif type_value == "OperationHard":
            value = node_item.get_value()
            # values = value.getLeftOperand()
            value = self.execute_hard_operation(value)
            self.variables_values[name_variable] = value

    def execute_print(self, node_item):
        type_value = node_item.get_type_value()
        if type_value == "INT":
            value = node_item.get_value_token()
            print(int(value[0].get_value_token()))
        elif type_value == "FLOAT":
            value = node_item.get_value_token()
            print(float(value[0].get_value_token()))
        elif type_value == "VAR":
            name_variable = node_item.get_value_node()[0].get_value_token()
            if name_variable in self.variables_values:
                value = self.variables_values[name_variable]
                print(f'{name_variable}: {value}')
            elif name_variable in self.linkedlist_values:
                value = self.linkedlist_values[name_variable]
                print(f'{name_variable}:', end=' ')
                value.show()
            else:
                Errors.error_message('Value of variable not found!')
        elif type_value == "ListVars":
            for item in node_item.get_value_node():
                type_value = item.get_type_token()
                value = item.get_value_token()
                if type_value == "INT":
                    print(int(value), end=" ")
                elif type_value == "FLOAT":
                    print(float(value), end=" ")
                elif type_value == "VAR":
                    name_variable = value
                    if name_variable in self.variables_values:
                        value = self.variables_values[name_variable]
                        print(f'{name_variable}: {value}', end=" ")
                    elif name_variable in self.linkedlist_values:
                        value = self.linkedlist_values[name_variable]
                        print(f'{name_variable}:', end=' ')
                        value.show()
                    else:
                        Errors.error_message('Value of variable not found!')
            print()
        else:
            Errors.error_message("Output only Integers, Float and Vars!")

    def execute_input(self, node_item):
        comment = node_item.get_comment()
        name_variable = node_item.get_name_variable()
        if comment is None:
            value = input(f"Entering the value of a variable '{name_variable}':")
        else:
            value = input(comment)
        self.variables_values[name_variable] = value

    def execute_if(self, node_item):
        condition = node_item.get_condition()
        loop = node_item.get_loop()
        value_one = condition[0]
        sign = condition[1]
        value_two = condition[2]
        # print("IF:", value_one.getTypeToken(), sign.getTypeToken(), value_two.getTypeToken())

        if value_one.get_type_token() == "VAR":
            value_one_condition = self.get_value_var(value_one.get_value_token())
        else:
            value_one_condition = value_one.get_value_token()

        if value_two.get_type_token() == "VAR":
            value_two_condition = self.get_value_var(value_two.get_value_token())
        else:
            value_two_condition = value_two.get_value_token()

        type_sign = sign.get_type_token()
        result = False
        if type_sign == "MORE":
            if int(value_one_condition) > int(value_two_condition):
                result = True
        elif type_sign == "LESS":
            if int(value_one_condition) < int(value_two_condition):
                result = True
        elif type_sign == "MORE_EQUALLY":
            if int(value_one_condition) >= int(value_two_condition):
                result = True
        elif type_sign == "LESS_EQUALLY":
            if int(value_one_condition) <= int(value_two_condition):
                result = True
        elif type_sign == "EQUALS":
            if int(value_one_condition) == int(value_two_condition):
                result = True
        elif type_sign == "NOT_EQUALLY":
            if int(value_one_condition) != int(value_two_condition):
                result = True

        if result:
            for node_loop in loop:
                node_type = node_loop.get_type_node()
                if node_type == "Print":
                    self.execute_print(node_loop)
                elif node_type == "Assign":
                    self.execute_assign(node_loop)
                else:
                    Errors.error_message("In 'if' only print and assign")

    def execute_while(self, node_item):
        while True:
            condition = node_item.get_condition()
            loop = node_item.get_loop()
            value_one = condition[0]
            sign = condition[1]
            value_two = condition[2]

            if value_one.get_type_token() == "VAR":
                value_one_condition = self.get_value_var(value_one.get_value_token())
            else:
                value_one_condition = value_one.get_value_token()

            if value_two.get_type_token() == "VAR":
                value_two_condition = self.get_value_var(value_two.get_value_token())
            else:
                value_two_condition = value_two.get_value_token()
            type_sign = sign.get_type_token()

            result = False
            if type_sign == "MORE":
                if int(value_one_condition) > int(value_two_condition):
                    result = True
                else:
                    break
            elif type_sign == "LESS":
                if int(value_one_condition) < int(value_two_condition):
                    result = True
                else:
                    break
            elif type_sign == "MORE_EQUALLY":
                if int(value_one_condition) >= int(value_two_condition):
                    result = True
                else:
                    break
            elif type_sign == "LESS_EQUALLY":
                if int(value_one_condition) <= int(value_two_condition):
                    result = True
                else:
                    break
            elif type_sign == "EQUALS":
                if int(value_one_condition) == int(value_two_condition):
                    result = True
                else:
                    break
            elif type_sign == "NOT_EQUALLY":
                if int(value_one_condition) != int(value_two_condition):
                    result = True
                else:
                    break

            if result:
                for node_loop in loop:
                    node_type = node_loop.get_type_node()
                    if node_type == "Print":
                        self.execute_print(node_loop)
                    elif node_type == "Assign":
                        self.execute_assign(node_loop)
                    else:
                        Errors.error_message("In 'while' only print and assign")

    def execute_for(self, node_item):
        condition = node_item.get_condition()
        value_one = condition[0]
        # sign = condition[1] # In Parser
        value_two = condition[2]
        loop = node_item.get_loop()
        name_variable = node_item.get_name_variable()

        if value_one.get_type_token() == "VAR":
            value_one_condition = self.get_value_var(value_one.get_value_token())
        else:
            value_one_condition = int(value_one.get_value_token())

        if value_two.get_type_token() == "VAR":
            value_two_condition = self.get_value_var(value_two.get_value_token())
        else:
            value_two_condition = int(value_two.get_value_token())

        if value_one_condition < value_two_condition:
            self.variables_values[name_variable] = value_one_condition
            while self.variables_values[name_variable] <= value_two_condition:
                for node_loop in loop:
                    node_type = node_loop.get_type_node()
                    if node_type == "Print":
                        self.execute_print(node_loop)
                    elif node_type == "Assign":
                        self.execute_assign(node_loop)
                    else:
                        Errors.error_message("In 'for' only print and assign")
                self.variables_values[name_variable] += 1
            del self.variables_values[name_variable]
        else:
            Errors.error_message("In condition 'for' the first value must be less than the second")

    def execute_operation(self, node_item):
        left = node_item.get_left_operand()
        right = node_item.get_right_operand()
        if left.get_type_token() == "VAR":
            left_operand = self.get_value_var(left.get_value_token())
        else:
            left_operand = left.get_value_token()

        if right.get_type_token() == "VAR":
            right_operand = self.get_value_var(right.get_value_token())
        else:
            right_operand = right.get_value_token()
        sign = node_item.get_sign()
        final = node_item.get_final()
        value = 0
        if final:
            if sign.get_type_token() == "PLUS_OP":
                value = int(left_operand) + int(right_operand)
            if sign.get_type_token() == "MINUS_OP":
                value = int(left_operand) - int(right_operand)
            if sign.get_type_token() == "MULTIPLICATION_OP":
                value = int(left_operand) * int(right_operand)
            if sign.get_type_token() == "SLASH_OP":
                value = int(left_operand) / int(right_operand)
            if sign.get_type_token() == "MOD_OP":
                value = int(left_operand) % int(right_operand)
            if sign.get_type_token() == "DIV_OP":
                value = int(left_operand) // int(right_operand)
        else:
            pass
        return int(value)

    @staticmethod
    def execute_hard_operation(node_item):
        values = node_item.get_left_operand()
        exp = [elem.get_value_token() for elem in values]
        # print("HARD:", exp)
        value = node_item.function(exp)
        return value

    def execute_linked_list(self, node_item):  # List class
        name = node_item.get_name()
        values = node_item.get_values()
        # new_values = [elem.getValue() for elem in values]
        new_values = List()
        for elem in values:
            new_values.add(elem.get_value_token())
        # new_values.show()
        self.linkedlist_values[name] = new_values

    def execute_linked_list_operation(self, node_item):
        type_operation = node_item.get_type_operation()

        if type_operation == "setLLInsertAtEnd":
            name_variable = node_item.get_name_variable()
            value = node_item.get_values()
            # value_type = value.getTypeToken()
            value = value.get_value_token()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                values.add(value)
                # self.linkedlist_values[name_variable] = values
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLInsertAtHead":
            name_variable = node_item.get_name_variable()
            value = node_item.get_values()
            # value_type = value.getTypeToken()
            value = value.get_value_token()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                values.add_head(value)
                # self.linkedlist_values[name_variable] = values
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLDelete":
            name_variable = node_item.get_name_variable()
            value = node_item.get_values()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                if value != "":
                    value = value.get_value_token()
                    values.dele(int(value))
                else:
                    values.dele(value)
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLDeleteAtHead":
            name_variable = node_item.get_name_variable()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                values.dele(0)
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLSearch":
            name_variable = node_item.get_name_variable()
            value = node_item.get_values()
            # value_type = value.getTypeToken()
            value = value.get_value_token()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                result = values.jogging(int(value))
                if result == -1:
                    Errors.error_message('List out of range')
                else:
                    result = result.get_value_node()
                    print(f"Element on position {value}: {result}")
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLIsEmpty":
            name_variable = node_item.get_name_variable()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                if values.size() == 0:
                    print(f"LinkedList {name_variable} is empty.")
                else:
                    print(f"LinkedList {name_variable} is NOT empty.")
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLLen":
            name_variable = node_item.get_name_variable()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                size = values.size()
                print(f'Size of {name_variable}: {size}')
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        else:
            pass
