from LinkList import *


class Interpreter:

    def __init__(self, node_list):
        self.node_list = node_list
        self.variables_values = dict()
        self.linkedlist_values = dict()

    def execute(self):
        for node in self.node_list:
            node_type = node.getTypeNode()
            # print("node_type:", node_type)
            if node_type == "Print":
                self.executePrint(node)
            elif node_type == "If":
                self.executeIf(node)
            elif node_type == "While":
                self.executeWhile(node)
            elif node_type == "For":
                self.executeFor(node)
            elif node_type == "Assign":
                self.executeAssign(node)
            elif node_type == "LinkedList":
                self.executeLinkedList(node)
            elif node_type == "LinkedListOperationNode":
                self.executeLinkedListOperation(node)
            else:
                print("ERROR(STRANGE)")

    def get_value_var(self, pos):
        try:
            result = self.variables_values[pos]
            return result
        except:
            Errors.error_message(f'Value of variable not found: {pos}')

    def executeAssign(self, node):
        name_variable = node.getNameVariable()
        type_value = node.getTypeValue()
        # print(name_variable, type_value)

        if type_value == "INT":
            value = node.getValue()[0].getValue()
            # print(name_variable, value, node.getValue(), node.getValue()[0], node.getValue()[0].getValue())
            self.variables_values[name_variable] = value
        elif type_value == "VAR":
            # print(value)
            value = node.getValue()[0].getValue()
            self.variables_values[name_variable] = self.get_value_var(value)
        elif type_value == "Operation":
            value = self.executeOperation(node.getValue())
            self.variables_values[name_variable] = value
        elif type_value == "OperationHard":
            value = node.getValue()
            # values = value.getLeftOperand()
            value = self.executeHardOperation(value)
            self.variables_values[name_variable] = value

    def executePrint(self, node):
        type_value = node.getTypeValue()
        if type_value == "INT":
            value = node.getValue()
            print(value[0].getValue())
        elif type_value == "FLOAT":
            value = node.getValue()
            print(value[0].getValue())
        elif type_value == "VAR":
            name_variable = node.getValue()[0].getValue()
            if name_variable in self.variables_values:
                value = self.variables_values[name_variable]
                print(f'{name_variable}: {value}')
            elif name_variable in self.linkedlist_values:
                value = self.linkedlist_values[name_variable]
                print(f'{name_variable}:', end=' ')
                value.show()
            else:
                Errors.error_message('Value of variable not found!')
        else:
            Errors.error_message("Output only Vars and Integers!")

    def executeIf(self, node):
        condition = node.getCondition()
        loop = node.getLoop()
        value_one = condition[0]
        sign = condition[1]
        value_two = condition[2]
        # print("IF:", value_one.getTypeToken(), sign.getTypeToken(), value_two.getTypeToken())

        if value_one.getTypeToken() == "VAR":
            value_one_condition = self.get_value_var(value_one.getValue())
        else:
            value_one_condition = value_one.getValue()

        if value_two.getTypeToken() == "VAR":
            value_two_condition = self.get_value_var(value_two.getValue())
        else:
            value_two_condition = value_two.getValue()

        type_sign = sign.getTypeToken()
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
                node_type = node_loop.getTypeNode()
                if node_type == "Print":
                    self.executePrint(node_loop)
                elif node_type == "Assign":
                    self.executeAssign(node_loop)
                else:
                    Errors.error_message("In 'if' only print and assign")

    def executeWhile(self, node):
        while True:
            condition = node.getCondition()
            loop = node.getLoop()
            value_one = condition[0]
            sign = condition[1]
            value_two = condition[2]

            if value_one.getTypeToken() == "VAR":
                value_one_condition = self.get_value_var(value_one.getValue())
            else:
                value_one_condition = value_one.getValue()

            if value_two.getTypeToken() == "VAR":
                value_two_condition = self.get_value_var(value_two.getValue())
            else:
                value_two_condition = value_two.getValue()
            type_sign = sign.getTypeToken()

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
                    node_type = node_loop.getTypeNode()
                    if node_type == "Print":
                        self.executePrint(node_loop)
                    elif node_type == "Assign":
                        self.executeAssign(node_loop)
                    else:
                        Errors.error_message("In 'while' only print and assign")

    def executeFor(self, node):
        condition = node.getCondition()
        value_one = condition[0]
        # sign = condition[1] # In Parser
        value_two = condition[2]
        loop = node.getLoop()
        name_variable = node.getNameVariable()

        if value_one.getTypeToken() == "VAR":
            value_one_condition = self.get_value_var(value_one.getValue())
        else:
            value_one_condition = int(value_one.getValue())

        if value_two.getTypeToken() == "VAR":
            value_two_condition = self.get_value_var(value_two.getValue())
        else:
            value_two_condition = int(value_two.getValue())

        if value_one_condition < value_two_condition:
            self.variables_values[name_variable] = value_one_condition
            while self.variables_values[name_variable] <= value_two_condition:
                for node_loop in loop:
                    node_type = node_loop.getTypeNode()
                    if node_type == "Print":
                        self.executePrint(node_loop)
                    elif node_type == "Assign":
                        self.executeAssign(node_loop)
                    else:
                        Errors.error_message("In 'for' only print and assign")
                self.variables_values[name_variable] += 1
            del self.variables_values[name_variable]
        else:
            Errors.error_message("In condition 'for' the first value must be less than the second")

    def executeOperation(self, node):
        left = node.getLeftOperand()
        right = node.getRightOperand()
        if left.getTypeToken() == "VAR":
            left_operand = self.get_value_var(left.getValue())
        else:
            left_operand = left.getValue()

        if right.getTypeToken() == "VAR":
            right_operand = self.get_value_var(right.getValue())
        else:
            right_operand = right.getValue()
        sign = node.getSign()
        final = node.getFinal()
        value = 0
        if final:
            if sign.getTypeToken() == "PLUS_OP":
                value = int(left_operand) + int(right_operand)
            if sign.getTypeToken() == "MINUS_OP":
                value = int(left_operand) - int(right_operand)
            if sign.getTypeToken() == "MULTIPLICATION_OP":
                value = int(left_operand) * int(right_operand)
            if sign.getTypeToken() == "SLASH_OP":
                value = int(left_operand) / int(right_operand)
            if sign.getTypeToken() == "MOD_OP":
                value = int(left_operand) % int(right_operand)
            if sign.getTypeToken() == "DIV_OP":
                value = int(left_operand) // int(right_operand)
        else:
            pass
        return int(value)

    def executeHardOperation(self, node):
        values = node.getLeftOperand()
        exp = [elem.getValue() for elem in values]
        value = node.function(exp)
        return value

    def executeLinkedList(self, node):  # List class
        name = node.getName()
        values = node.getValues()
        # new_values = [elem.getValue() for elem in values]
        new_values = List()
        for elem in values:
            new_values.add(elem.getValue())
        # new_values.show()
        self.linkedlist_values[name] = new_values

    def executeLinkedListOperation(self, node):
        type_operation = node.getTypeOperation()

        if type_operation == "setLLInsertAtEnd":
            name_variable = node.getNameVariable()
            value = node.getValues()
            # value_type = value.getTypeToken()
            value = value.getValue()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                values.add(value)
                # self.linkedlist_values[name_variable] = values
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLInsertAtHead":
            name_variable = node.getNameVariable()
            value = node.getValues()
            # value_type = value.getTypeToken()
            value = value.getValue()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                values.add_head(value)
                # self.linkedlist_values[name_variable] = values
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLDelete":
            name_variable = node.getNameVariable()
            value = node.getValues()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                if value != "":
                    value = value.getValue()
                    values.dele(int(value))
                else:
                    values.dele(value)
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLDeleteAtHead":
            name_variable = node.getNameVariable()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                values.dele(0)
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLSearch":
            name_variable = node.getNameVariable()
            value = node.getValues()
            # value_type = value.getTypeToken()
            value = value.getValue()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                result = values.jogging(int(value))
                if result == -1:
                    Errors.error_message('List out of range')
                else:
                    result = result.get_value()
                    print(f"Element on position {value}: {result}")
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLIsEmpty":
            name_variable = node.getNameVariable()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                if values.size() == 0:
                    print(f"LinkedList {name_variable} is empty.")
                else:
                    print(f"LinkedList {name_variable} is NOT empty.")
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        elif type_operation == "setLLLen":
            name_variable = node.getNameVariable()
            if name_variable in self.linkedlist_values:
                values = self.linkedlist_values[name_variable]
                size = values.size()
                print(f'Size of {name_variable}: {size}')
            else:
                Errors.error_message('Value of variable not found: ' + str(name_variable))

        else:
            pass
