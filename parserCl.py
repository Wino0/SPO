class parserCl:
    def __init__(self, lexer):
        self.height = 0
        self.i = 0
        self.start = lexer
        self.LB = 0

    def S(self):
        S = Node('S')
        while self.i < len(self.start) - 1:
            self.height = 1
            expr = self.expr()
            if expr is not None:
                S.children.append(expr)
            self.i += 1
        return S

    def if_expr(self):
        height = self.height
        if_expr = Node('if_expr', height=self.height)
        self.height += 1
        start_height = self.height
        self.check_next('LBreaket')
        if_expr.children.append(Leaf('LBreaket', '(', height=self.height))
        self.i += 2
        self.height += 1
        token = list(self.start[self.i].keys())[0]

        if token == 'VAR' or token == 'NUMBER' or token == 'LBreaket':
            math_logic = self.math_logic(ht=[start_height])
            if_expr.children.append(math_logic)

            self.height = start_height
            self.check_next('LFBreaket')
            if_expr.children.append(Node('LFBreaket', height=start_height))
            self.i += 1
            num_L = 1
            while num_L:
                if list(self.start[self.i].keys())[0] == 'RFBreaket':
                    num_L -= 1
                if list(self.start[self.i].keys())[0] == 'LFBreaket':
                    num_L += 1
                if num_L:
                    self.i += 1
                    self.height = start_height
                    self.height += 1
                    if list(self.start[self.i].keys())[0] == 'LFBreaket':
                        num_L += 1
                    if list(self.start[self.i].keys())[0] == 'RFBreaket':
                        num_L -= 1
                        break
                    expr = self.expr()
                    if expr is not None:
                        if_expr.children.append(expr)

            if_expr.children.append(Node('RFBreaket', height=start_height))

            if self.i < len(self.start) - 1:
                self.check_next('ELSE')
                self.i += 1
                self.check_next('LFBreaket')
                self.height = height
                if_expr.children.append(Node('ELSE', height=self.height))
                self.height += 1
                start_height = self.height
                if_expr.children.append(Node('LFBreaket', height=self.height))
                num_L = 1

                while num_L:
                    if list(self.start[self.i].keys())[0] == 'RFBreaket':
                        num_L -= 1
                    if list(self.start[self.i].keys())[0] == 'LFBreaket':
                        num_L += 1
                    if num_L:
                        self.i += 1
                        self.height = start_height
                        self.height += 1
                        if list(self.start[self.i].keys())[0] == 'LFBreaket':
                            num_L += 1
                        if list(self.start[self.i].keys())[0] == 'RFBreaket':
                            num_L -= 1
                            break
                        expr = self.expr()
                        if expr is not None:
                            if_expr.children.append(expr)
                if_expr.children.append(Node('RFBreaket', height=start_height))
            return if_expr



    def method(self):
        method = Node('method', height=self.height)
        self.height += 1
        self.check_next('METHOD')
        self.i += 1
        method.children.append(Leaf(name=list(self.start[self.i].keys())[0], value=list(self.start[self.i].values())[0],
                               height=self.height))
        self.height += 1
        self.check_next('LBreaket')
        self.i += 1
        method.children.append(Leaf(name=list(self.start[self.i].keys())[0], value=list(self.start[self.i].values())[0],
                                    height=self.height))
        math_expr = self.math_expr()
        method.children.append(math_expr)
        if not list(self.start[self.i].keys())[0] == 'END_COM':
            raise BaseException
        return method

    def while_expr(self):
        while_expr = Node('while_expr', height=self.height)
        self.height += 1
        start_height = self.height
        self.check_next('LBreaket')
        while_expr.children.append(Leaf('LBreaket', '(', height=self.height))
        self.i += 2
        self.height += 1
        token = list(self.start[self.i].keys())[0]
        if token == 'VAR' or token == 'NUMBER' or token == 'LBreaket':
            math_logic = self.math_logic(ht=[start_height])
            while_expr.children.append(math_logic)
            self.height = start_height
            self.check_next('LFBreaket')
            self.i += 1
            while_expr.children.append(Node('LFBreaket', height=self.height))
            num_L = 1

            while num_L:
                if list(self.start[self.i].keys())[0] == 'RFBreaket':
                    num_L -= 1
                if list(self.start[self.i].keys())[0] == 'LFBreaket':
                    num_L += 1
                if num_L:
                    self.i += 1
                    self.height = start_height
                    self.height += 1
                    if list(self.start[self.i].keys())[0] == 'LFBreaket':
                        num_L += 1
                    if list(self.start[self.i].keys())[0] == 'RFBreaket':
                        num_L -= 1
                        break
                    expr = self.expr()
                    if expr is not None:
                        while_expr.children.append(expr)
            while_expr.children.append(Node('RFBreaket', height=start_height))
            return while_expr
        else:
            raise BaseException

    def expr(self):
        try:
            expr = Node('expr', height=self.height)
            self.height += 1
            token = list(self.start[self.i].keys())[0]
            if token == "VAR":
                try:
                    assign_expr = self.assign_expr()
                    expr.children.append(assign_expr)
                    self.height -= 1
                    return expr
                except BaseException:
                    expr.children.append(Leaf(list(self.start[self.i].keys())[0], list(self.start[self.i].values())[0],
                                              self.height))
                    self.check_next('POINT')
                    self.i += 1
                    method = self.method()
                    expr.children.append(method)
                    return expr
            elif token == 'WHILE':
                while_expr = self.while_expr()
                expr.children.append(while_expr)
                self.height -= 1
                return expr
            elif token == 'IF':
                if_expr = self.if_expr()
                expr.children.append(if_expr)
                self.height -= 1
                return expr
            else:
                return None
        except BaseException:
            raise BaseException

    def math_logic(self, ht=[]):
        token = list(self.start[self.i].keys())[0]
        if not token == 'RBreaket' or not token == 'LOGICAL_OP' \
                or not token == 'OP':
            math_logic = Node('math_logic', height=self.height)
        else:
            math_logic = ''
        self.height += 1
        if token == 'LBreaket':
            ht.append(self.height)
            LBreaket = self.LBreaket()
            math_logic.children.append(LBreaket)
        elif token == 'RBreaket':
            self.height = ht.pop(-1)
            math_logic = Node('RBreaket',  height=self.height)
        elif token == 'NUMBER':
            math_logic.children.append(Leaf(list(self.start[self.i].keys())[0],
                                            list(self.start[self.i].
                                                 values())[0],
                                            self.height))
            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'LOGICAL_OP':
                    self.i += 1
                    math_logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))
                elif list(self.start[self.i + 1].keys())[0] == 'OP':
                    self.i += 1
                    math_logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))
        elif token == 'VAR':
            math_logic.children.append(Leaf(list(self.start[self.i].keys())[0],
                                            list(self.start[self.i].
                                                 values())[0],
                                            self.height))
            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'LOGICAL_OP':
                    self.i += 1
                    math_logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))
                elif list(self.start[self.i + 1].keys())[0] == 'OP':
                    self.i += 1
                    math_logic.children.append(Leaf(list(self.start[self.i].
                                                         keys())[0],
                                                    list(self.start[self.i].
                                                         values())[0],
                                                    self.height))
        elif token == 'LOGICAL_OP':
            self.height -= 1
            math_logic = Node('LOGICAL_OP' +
                              list(self.start[self.i].values())[0],
                              height=self.height)
        elif token == 'OP':
            self.height -= 1
            math_logic = Node('OP' + list(self.start[self.i].values())[0],
                              height=self.height)
        elif not token == 'END_COM':
            raise BaseException
        if len(ht):
            self.i += 1
            me = self.math_logic(ht)
            math_logic.children.append(me)
        return math_logic

    def check_next(self, values):
        token = list(self.start[self.i + 1].keys())[0]
        if not token == values:
            raise BaseException

    def assign_expr(self):
        assign_expr = Node('assign_expr', '=', self.height)
        self.check_next("ASSIGN_OP")
        self.height += 1
        assign_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                         list(self.start[self.i].
                                              values())[0], self.height))
        self.i += 1
        assign_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                         list(self.start[self.i].
                                              values())[0], self.height))
        self.height -= 1
        self.i += 1
        token = list(self.start[self.i].keys())[0]
        if token == 'STR':
            self.height += 1
            assign_expr.children.append(Leaf('STR', list(self.start[self.i].
                                                         values())[0],
                                             self.height))
            self.check_next('END_COM')
            self.i += 1

        elif token == 'NUMBER' or token == 'LBreaket' or token == 'VAR':
            self.height += 1
            math_expr = self.math_expr()
            assign_expr.children.append(math_expr)

        elif token == 'LINKED_LIST_KW':
            self.height += 1
            assign_expr.children.append(Leaf('LINKED_LIST_KW', list(self.start[self.i].values())[0], self.height))

        return assign_expr

    def math_expr(self, ht=[]):
        token = list(self.start[self.i].keys())[0]
        if not token == 'RBreaket' or not token == 'OP' or not token == 'POINT':
            math_expr = Node('math_expr', height=self.height)
        else:
            math_expr = ''
        self.height += 1

        if token == 'LBreaket':
            ht.append(self.height)
            LBreaket = self.LBreaket()
            math_expr.children.append(LBreaket)

        elif token == 'RBreaket':
            self.LB -= 1
            self.height = ht.pop(-1)
            if self.LB < 0:
                raise BaseException
            math_expr = Node('RBreaket', value=')', height=self.height)

        elif token == 'NUMBER':
            math_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                           list(self.start[self.i].
                                                values())[0],
                                           self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'OP':
                    self.i += 1
                    math_expr.children.append(Leaf(list(self.start[self.i].
                                                        keys())[0],
                                                   list(self.start[self.i].
                                                        values())[0],
                                                   self.height))

        elif token == 'OP':
            self.height -= 1
            math_expr = Node('OP' + list(self.start[self.i].values())[0],
                             height=self.height)

        elif token == 'VAR':
            math_expr.children.append(Leaf(list(self.start[self.i].keys())[0],
                                           list(self.start[self.i].
                                                values())[0],
                                           self.height))

            if self.i + 1 < len(self.start):
                if list(self.start[self.i + 1].keys())[0] == 'OP':
                    self.i += 1
                    math_expr.children.append(Leaf(list(self.start[self.i].
                                                        keys())[0],
                                                   list(self.start[self.i].
                                                        values())[0],
                                                   self.height))

        elif token == 'POINT':
            math_expr = self.method()
            self.i -= 1
        elif not token == 'END_COM':
            raise BaseException

        self.i += 1
        if not list(self.start[self.i].keys())[0] == 'END_COM':
            me = self.math_expr(ht)
            math_expr.children.append(me)

        return math_expr

    def LBreaket(self):
        self.LB += 1
        LBreaket = Leaf('LBreaket', '(', height=self.height)

        return LBreaket


class Node:
    def __init__(self, name='', value='', height=0):
        self.children = []
        self.name = name
        self.value = value
        self.height = height
        self.buffer = []

    def __repr__(self):
        str_end = ''
        for child in self.children:
            str_end += "\t" * child.height + f'{child}'
        return f'{self.name}\n{str_end}'


class Leaf:
    def __init__(self, name='', value='', height=0):
        self.name = name
        self.value = value
        self.height = height

    def __repr__(self):
        return f'{self.name} {self.value}\n'