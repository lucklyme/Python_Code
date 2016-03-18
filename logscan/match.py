import re


class Token:
    LEFT_BRACKETS = 'LEFT_BRACKETS'
    RIGHT_BRACKETS = 'RIGHT_BRACKETS'
    SYMBOL = 'SYMBOL'
    EXPRESSION = 'EXPRESSION'
    SYMBOLS = '&|!'

    def __init__(self, value, type):
        self.value = value
        self.type = type


class ASTree:
    def __init__(self, token):
        self.root = token
        self.right = None
        self.left = None


def tokenize(origin):
    tokens = []
    expr = []
    is_expr = False
    for c in origin:
        if c == '#' and is_expr is False:
            is_expr = True
        elif c == '#' and is_expr is True:
            is_expr = False
            token = Token(''.join(expr), Token.EXPRESSION)
            tokens.append(token)
            expr = []
        elif is_expr is True:
            expr.append(c)
        elif c in Token.SYMBOLS:
            token = Token(c, Token.SYMBOL)
            tokens.append(token)
        elif c == '(':
            token = Token(c, Token.LEFT_BRACKETS)
            tokens.append(token)
        elif c == ')':
            token = Token(c, Token.RIGHT_BRACKETS)
            tokens.append(token)
    return tokens


def make_ast(tokens):
    stack = []
    for t in tokens:
        tree = ASTree(t)
        if tree.root.type == Token.SYMBOL or tree.root.type == Token.LEFT_BRACKETS:
            stack.append(tree)
        elif tree.root.type == Token.EXPRESSION:
            make_sub_ast(stack, tree)
        else:
            sub_tree = stack.pop()
            if sub_tree.root.type != Token.SYMBOL and sub_tree.root.type != Token.EXPRESSION:
                raise Exception('parse error, excepted {0} or {1} but {2}'.format(Token.SYMBOL,
                                                                                  Token.EXPRESSION, sub_tree))
            tmp = stack.pop()
            if tmp.root.tpye != Token.LEFT_BRACKETS:
                raise Exception('paser error, excepted {0} but {1}'.format(Token.LEFT_BRACKETS, tmp))
            make_sub_ast(stack, sub_tree)
    return stack.pop()


def make_sub_ast(stack, t):
    current = t
    while stack and stack[-1].root.type != Token.LEFT_BRACKETS:
        node = stack.pop()
        if node.root.type != Token.SYMBOL:
            raise Exception('parse error, excepted {0} but {1}'.format(Token.SYMBOL, node.root))
        node.right = current
        if node.root.value in '&|':
            left = stack.pop()
            if left.root.type != Token.EXPRESSION and left.root.type != Token.SYMBOL:
                raise Exception('parse error, excepted {0} or {1} but {2}'.format(Token.SYMBOL,
                                                                                  Token.EXPRESSION, left.root))
            node.left = left
        current = node
    stack.append(current)


def cacl(ast, line):
    if ast.root.type != Token.EXPRESSION:
        if ast.root.value == '!':
            return not cacl(ast.right, line)
        elif ast.root.value == '&':
            return cacl(ast.left, line) and cacl(ast.right, line)
        elif ast.root.value == '|':
            return cacl(ast.left, line) or cacl(ast.right, line)
    else:
        return re.search(ast.root.value, line) is not None


class Match:
    def __init__(self, origin):
        self.origin = origin
        self.ast = make_ast(tokenize(origin))

    def match(self, line):
        return cacl(self.ast, line)


if __name__ == '__main__':
    lines = '传呼期间在设备 \Device\Harddisk2\DR5 上检测到一个错误。'
    exprs = '#\\D\D{5}# & #D.\d#'

    m = Match(exprs)
    print(m.match(lines))







