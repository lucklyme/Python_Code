from stack import Stack


def cacl(expr):
    dict1 = {')': '(', ']': '[', '}': '{'}
    c = ""
    isint = False
    for i in expr:
        if i in '(,[,{,),],},+,-,/,*':
            c = c + ' ' + i
            isint = False
        elif i == ' ':
            pass
        elif i == '.':
            c = c + i
        elif isinstance(int(i), int) and isint is False:
            c = c + ' ' + i
            isint = True
        else:
            c = c + i
    ''' 以上代码是将表达式中插入空格，以方便后续根据空格拆分'''
    expr_list = c.split(" ")
    expr_list.pop(0)
    '''以下代码功能：将括号内的数据压入栈1，然后调用cacl1方法进行优先计算，得到的值再压回栈'''
    for n in expr_list:
        if n not in '),],}':
            stack.push(n)
        elif n in '),],}':
            while stack.top.value != dict1[n]:
                if stack.top.value in '+,-,*,/':
                    stack1.push(stack.pop())
                elif isinstance(float(stack.top.value), float):
                    stack1.push(stack.pop())
                else:
                    raise Exception('wrong expr')
            else:
                stack.pop()
                num = cacl1(stack1)
                stack.push(str(num))
    else:
        '''翻转栈中数据的顺序，使得保持原算式顺序不变'''
        while stack.top:
            stack1.push(stack.pop())
        return cacl1(stack1)


'''以下方法将栈1中的数据压入栈2，当遇到* 和 / 优先计算，将结果压入栈2'''


def cacl1(stack1):
    while stack1.top:
        if stack1.top.value not in '*,/':
            stack2.push(stack1.pop())
        elif stack1.top.value in '*,/':
            operator = stack1.pop()
            num1 = float(stack2.pop())
            num2 = float(stack1.pop())
            score = func_map[operator](num1, num2)
            stack2.push(score)
    '''翻转栈2中的数据到栈1，保持算式顺序不变，并将计算其中的加减法，并返回值'''
    while stack2.top:
        stack1.push(stack2.pop())
    while stack1.top:
        num1 = float(stack1.pop())
        if stack1.top is None:
            return num1
        if stack1.top.value in '+,-':
            operator = stack1.pop()
            num2 = float(stack1.pop())
            score = func_map[operator](num1, num2)
            stack1.push(score)
    return score


func_map = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

if __name__ == '__main__':
    stack = Stack()
    stack1 = Stack()
    stack2 = Stack()
    print(cacl('((((5*5.5)+(6*6)/8*(9+9.6*9))*5)/8)*8'))

