#!/usr/bin/env python
#coding=utf-8

V = None
T = None
P = None
S = None

def getGrammar():
    global V, T, P, S
    a = raw_input('Please input the V:')
    V = set([x for x in a.split(' ')])

    a = raw_input('Please input the T:')
    T = set([x for x in a.split(' ')])

    P = []
    a = raw_input('Please input the P:\n>>> ')
    while a != "":
        tmp = a.strip().split(' ')
        P.append(tmp)
        a = raw_input('>>> ')

    a = raw_input('Please input the S:')
    S = a

def getFirst(X):
    first = set()
    if X in T:
        first.add(X)
        return first
    else:
        for item in P:
            if X == item[0]:
                if item[2] in T:
                    first.add(item[2])
                else:
                    first = first.union(getFirst(item[2]))
    return first

def getClosure(I):
    closure = []
    closure.extend(I)
    closure2 = closure[:]
    for item in closure2:
        latter = item.index('.')+1
        if item[latter] in T:
            tmp = item[:]
            tmp.remove('.')
            tmp.insert(latter,'.')
            tmp.pop()
            if latter+1 < len(item):
                tmp.append(getFirst(item[latter]))
            closure.append(tmp)
        else:
            for item2 in P:
                if item2[0] == item[latter]:
                    tmp = item2[:]
                    tmp.insert(tmp.index('->')+1,'.')
                    if latter+1 < len(item):
                        tmp.append(getFirst(item[latter]))
                    closure.append(tmp)
    return closure

def go(I,X):
    j = []
    for item in I:
        tmp = item[:]
        if item[item.index('.')+1] == X:
            tmp2 = tmp.index('.')
            tmp.remove('.')
            tmp.insert(tmp2+1,'.')
            j.append(tmp)
    return getClosure(j)


if __name__ == '__main__':
    getGrammar()
    # print getFirst('A')
    # print getClosure([['A','->','.','C','B','#']])
    print go([['A','->','.','C','B','#']],'C')