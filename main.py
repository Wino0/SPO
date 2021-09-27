from lexerCl import lexerCl
from stackMacCl import stackMacCl
from parserCl import parserCl

if __name__ == '__main__':
    L = lexerCl()
    L.term_getter('input.txt')
    print('Token:\n', L.list_tokens,'\n')
    try:
        P = parserCl(L.list_tokens)
        Tree = P.S()
        print('Tree:\n', Tree, '\n')
        StackMachine = stackMacCl(Tree.children)
        print('Polish inverted notation:')
        StackMachine.start()
    except BaseException:
        print('Syntax error')