import Errors


class Object:

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __del__(self):
        # print(self.get_value(), "DELETED")
        # print("del:self:", self.get_value())
        # print("del:next:", self.next.get_value())
        # print("del:prev:", self.prev.get_value())
        # del self
        pass

    def get_value(self):
        return self.value


class List:
    count = 0

    def __init__(self):
        self.first = None
        self.last = None
        List.count += 1
        self.count = List.count

    def size(self):  # Возврат размера списка
        if self.first != None:
            size = 1
            ob = self.first
            while ob.next != None:
                ob = ob.next
                size += 1
            return size
        else:
            return 0

    def free(self, obj):  # Освободить элемент от ссылок до удаления
        if obj.next != None and obj.prev != None:
            obj.prev.next = obj.next
            obj.next.prev = obj.prev
        if obj.next is None and obj.prev != None:
            self.last = obj.prev
            obj.prev.next = None
        if obj.next != None and obj.prev is None:
            self.first = obj.next
            obj.next.prev = None
        # del self

    def add(self, value):  # Добавление значения в конец списка
        ob = Object(value)
        if self.first is None:
            self.first = ob
        else:
            self.last.next = ob
            ob.prev = self.last
        self.last = ob

    def add_head(self, value):  # Добавление значения в начало списка
        ob = Object(value)
        ob.next = self.first
        if self.first is None:
            self.last = ob
        else:
            self.first.prev = ob
        self.first = ob

    def dele(self, pos):  # Удаление по индексу или же последнего
        if pos != "":
            ob = self.jogging(pos)
        else:
            ob = self.last

        if ob == -1:
            Errors.error_message('List out of range')
        else:
            pos = ob.get_value()
            self.free(ob)
            # del ob
            print(f"Element is deleted: {pos}")

    def show(self):  # Вывод списка
        if self.first != None:
            ob = self.first
            print('[', end='')
            while ob.next != None:
                print(ob.get_value(), end=', ')
                ob = ob.next
            print(str(ob.get_value()) + ']')
        else:
            print('[]')

    def jogging(self, pos):  # Пробежка по значениям и вытаскивание нужного по индексу
        size = self.size()
        if self.first != None:
            i = 0
            ob = self.first
            while i < size:
                # print("i:", i, pos, ob.get_value())
                if pos == i:
                    return ob
                i += 1
                ob = ob.next
        return -1

    def last_el(self):  # Возврат последнего элемента списка
        if self.first != None:
            ob = self.first
            while ob.next != None:
                ob = ob.next
            return ob
        else:
            return None
