
def checknone(fn):
    def wrap(*args, **kwargs):
        if args[0].head is None:
            print('this link is None')
            return
        else:
            return fn(*args, **kwargs)
    return wrap


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkList:
    def __init__(self):
        self.head = None
        self.end = None

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.end = new_node
        else:
            self.end.next = new_node
            self.end = new_node

    @checknone
    def insert(self, lst_id, value):
        cur = self.head
        cur_id = 0
        if lst_id == 0:
            node1 = Node(value)
            node1.next = self.head
            self.head = node1
        else:
            while cur_id < lst_id - 1:
                cur = cur.next
                if cur is None:
                    raise Exception('list length is less than lst_id')
                cur_id += 1
            node2 = Node(value)
            node2.next = cur.next
            cur.next = node2
            if node2.next is None:
                self.end = node2

    @checknone
    def remove(self, lst_id):
        cur = self.head
        cur_id = 0
        if lst_id == 0:
            self.head = cur.next
        else:
            while cur_id < lst_id - 1:
                cur = cur.next
                if cur is None:
                    raise Exception('list length is less than lst_id')
                cur_id += 1
            cur.next = cur.next.next
            if cur.next is None:
                self.end = cur

    def iter(self):
        cur = self.head
        if cur is None:
            return
        else:
            while cur is not None:
                yield cur.data
                cur = cur.next

    @checknone
    def pop(self, data):
        cur = self.head
        if cur.data == data:
            self.head = cur.next
            print('{0} has been poped'.format(cur.data))
        else:
            while cur.next is not None:
                if cur.next.data == data:
                    if cur.next.next is not None:
                        print('{0} has been poped'.format(cur.next.data))
                        cur.next = cur.next.next
                        return
                    else:
                        print('{0} has been poped'.format(cur.next.data))
                        cur.next = None
                        self.end = cur
                        return
                cur = cur.next

    def __len__(self):
        cur = self.head
        cur_num = 0
        while cur is not None:
            cur_num += 1
            cur = cur.next
        return cur_num


if __name__ == '__main__':
    linked_list = LinkList()
    for i in range(20):
        linked_list.append(i)

    linked_list.insert(0, 30)

    linked_list.remove(9)

    linked_list.pop(19)

    for node in linked_list.iter():
        print(node)
    print('this link length is {0}'.format(len(linked_list)))
