#!/usr/bin/env python
#coding=utf-8
import sys

def is_keyword(token):
    keywords = ['int','float','char','short','long','if','else','while','for','return']
    try:
        if keywords.index(token) > -1:
            return True
    except ValueError:
        return False

def get_token(filename):
    f = open(filename)
    buf = f.read()

    start = 0
    cur = 0

    while(cur < len(buf) - 1):
        start = cur
        c = buf[cur]
        while(c==" " or c=="\t" or c=="\n"):
            cur = cur + 1
            start = start + 1
            c = buf[cur]

        if c.isdigit():
            cur = cur + 1
            c = buf[cur]
            while(c.isdigit()):
                cur = cur + 1
                c = buf[cur]
            print "(CONST,%s)" % buf[start:cur]
            cur = cur - 1
        elif c.isalpha():
            cur = cur + 1
            c = buf[cur]
            while(c.isalnum()):
                cur = cur + 1
                c = buf[cur]
            if is_keyword(buf[start:cur]):
                print "(%s,0)" % buf[start:cur].upper()
            else:
                print "(IDENT,%s)" % buf[start:cur]
            cur = cur - 1
        else:
            if c == "*":
                cur = cur + 1
                c = buf[cur]
                if c == "*":
                    print "(EXP,0)"
                else:
                    cur = cur - 1
                    print "(MULTI,0)"
            elif c == ":":
                print "(COLON, 0)"
            elif c == "=":
                print "(ASSIGN, 0)"
            elif c == "%":
                print "(MOD, 0)"
            elif c == "&":
                print "(ADDR,0)"
            elif c == "[":
                print "(LM_BRAC,0)"
            elif c == "]":
                print "(RM_BRAC,0)"
            elif c == "+":
                print "(ADD,0)"
            elif c == "-":
                print "(MINUS,0)"
            elif c == "/":
                print "(DIV,0)"
            elif c == "<":
                print "(LT,0)"
            elif c == ">":
                print "(GT,0)"
            elif c == ";":
                print "(SEMIC,0)"
            elif c == ",":
                print "(COMMA,0)"
            elif c == "#":
                print "(PSEUDO_INS,0)"
            elif c == "'":
                print "(',0)"
            elif c == '"':
                cur = cur + 1
                c = buf[cur]
                while(c != '"'):
                    cur = cur + 1
                    c = buf[cur]
                print "(CONST,%s)" % buf[start:cur+1]
            elif c == ".":
                print "(DOT,0)"
            elif c == "(":
                print "(L_BRAC,0)"
            elif c == ")":
                print "(R_BRAC,0)"
            elif c == "}":
                print "(RB_BRAC,0)"
            elif c == "{":
                print "(LB_BRAC,0)"
            else:
                print "error"
        cur = cur + 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s filename" % sys.argv[0]
        sys.exit(-1)
    get_token(sys.argv[1])

