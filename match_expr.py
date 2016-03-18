"""
    本代码实现正则表达规则解析。
    定义#开头，#结尾的内容为正则表达，
    对匹配后得到的bool值，通过压栈，分步完成与、或、非操作
"""

from stack import Stack
import re


def match_expr(exprs, lines):
    stack = Stack()
    stack1 = Stack()
    expr = []
    isexpr = False
    for c in exprs:
        if c != '#' and isexpr is False and c != ' ':
            stack.push(c)
        elif c != '#' and isexpr is True:
            expr.append(c)
        elif c == '#' and isexpr is False:
            isexpr = True
        elif c == '#' and isexpr is True:
            isexpr = False
            ret = fn(lines, ''.join(expr))
            expr = []
            if stack.top is not None:
                if stack.top.value == '!':
                    stack.pop()
                    ret = not ret
                    stack.push(ret)
                    continue
            stack.push(ret)
            continue
        elif c == ')' and isexpr is False:
            while stack.top.value != '(':
                stack1.push(stack.pop())
            ret = match_expr1(stack1)
            if stack.top is not None and stack.top.value == '(':
                stack.pop()
            stack.push(ret)
    else:
        while stack.top:
                stack1.push(stack.pop())
        ret = match_expr1(stack1)
        return ret


def match_expr1(stack1):
    while stack1.top:
        if isinstance(stack1.top.value, bool):
            v = stack1.pop()
            if stack1.top is None:
                return v
        else:
            raise Exception('wrong expr')
        if stack1.top.value not in '&,|':
            raise Exception('wrong expr')
        else:
            s = stack1.pop()
            if isinstance(stack1.top.value, bool):
                ret = func_map[s](v, stack1.pop())
                stack1.push(ret)

func_map = {
    '|': lambda x, y: x or y,
    '&': lambda x, y: x and y,
}


def fn(str_lines, expr):
    pattern = re.compile(expr)
    match = re.search(pattern, str_lines)
    if match:
        return True
    else:
        return False

if __name__ == "__main__":
    lines = '传呼期间在设备 \Device\Harddisk2\DR5 上检测到一个错误。'
    exprs = '#\\D\D{5}# & #D.\d#'
    print(match_expr(exprs, lines, fn))
