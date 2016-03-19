from functools import partial
from stack import Stack


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self, node=None):
        self.root = node

    def add_left(self, tree):
        self.root.left = tree

    def add_right(self, tree):
        self.root.right = tree

    @property
    def left(self):
        return self.root.left

    @property
    def right(self):
        return self.root.right

    def visit_first(self, fn):
        fn(self.root.value)
        if self.left:
            self.left.visit_first(fn)
        if self.right:
            self.right.visit_first(fn)

    def visit_middle(self, fn):
        if self.left:
            self.left.visit_middle(fn)
        fn(self.root.value)
        if self.right:
            self.right.visit_middle(fn)

    def visit_last(self, fn):
        if self.left:
            self.left.visit_last(fn)
        if self.right:
            self.right.visit_last(fn)
        fn(self.root.value)

    def visit_iter_first(self, fn):
        stack = Stack()
        stack.push(self)
        while stack.top is not None:
            p = stack.pop()
            fn(p.root.value)
            if p.right is not None:
                stack.push(p.right)
            if p.left is not None:
                stack.push(p.left)

    def visit_iter_middle(self, fn):
        stack = Stack()
        tmp = []
        if self.right is not None:
            stack.push(self.right)
        stack.push(self)
        tmp.append(self.root.value)
        if self.left is not None:
            stack.push(self.left)
        while stack.top:
            p = stack.pop()
            if p.right is not None and p.root.value not in tmp:
                stack.push(p.right)
            stack.push(p)
            if p.left is not None and p.root.value not in tmp:
                stack.push(p.left)
                tmp.append(p.root.value)
            else:
                v = stack.pop()
                fn(v.root.value)

    def visit_iter_last(self, fn):
        stack = Stack()
        tmp = []
        stack.push(self)
        tmp.append(self.root.value)
        if self.right is not None:
            stack.push(self.right)
        if self.left is not None:
            stack.push(self.left)
        while stack.top:
            p = stack.pop()
            stack.push(p)
            if p.right is not None and p.root.value not in tmp:
                stack.push(p.right)
            if p.left is not None and p.root.value not in tmp:
                stack.push(p.left)
                tmp.append(p.root.value)
            else:
                v = stack.pop()
                fn(v.root.value)

if __name__ == '__main__':
    a = Tree(Node('A'))
    b = Tree(Node('B'))
    c = Tree(Node('C'))
    d = Tree(Node('D'))
    e = Tree(Node('E'))
    f = Tree(Node('F'))
    g = Tree(Node('G'))
    a.add_left(b)
    a.add_right(c)
    b.add_left(d)
    b.add_right(e)
    c.add_left(f)
    c.add_right(g)

    # p = partial(print, end='')
    # print('先序遍历：')
    # a.visit_first(p)
    # print('\n中序遍历：')
    # a.visit_middle(p)
    # print('\n后序遍历：')
    # a.visit_last(p)

    p = partial(print, end='')
    a.visit_iter_last(p)
