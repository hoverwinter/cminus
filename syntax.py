#!/usr/bin/env python
#coding=utf-8

def getCFG():
    a = raw_input('Please input the V:')
    b = set([x for x in a.split(' ')])
    print b

if __name__ == '__main__':
    getCFG()
