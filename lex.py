#!/usr/bin/env python
#coding=utf-8
import sys

tokens = [] #符号串 [[type,value],[type,value],...]

def keyword_index(t):
	keywords = ['break','continue','else','float','for','if','int','return','void','while','printf','scanf','main','function']
	try:
		tmp = keywords.index(t)
		if tmp < 10:
			return tmp+1
		else:
			return tmp+31
	except ValueError:
		return -1

def get_token(filename):
	global tokens
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
			tokens.append(['num',int(buf[start:cur])])
			print "(CONST,%s)" % buf[start:cur]
			cur = cur - 1
		elif c.isalpha() or c == '_':
			cur = cur + 1
			c = buf[cur]
			while(c.isalnum() or c == '_'):
				cur = cur + 1
				c = buf[cur]
			key_tmp = keyword_index(buf[start:cur])
			if key_tmp != -1:
				tokens.append([buf[start:cur],buf[start:cur]])
				print "(%s,0)" % buf[start:cur].upper()
			else:
				tokens.append(['id',buf[start:cur]])
				print "(IDENT,%s)" % buf[start:cur]
			cur = cur - 1
		else:
			if c == "+":
				c = buf[cur+1]
				if c == '+':
					tokens.append(['++','++'])
					cur += 1
					print "(INC,-1)"
				else:
					tokens.append(['+','+'])
					print "(ADD,0)"
			elif c == "-":
				tokens.append(['-','-'])
				print "(MINUS, 0)"
			elif c == "*":
				tokens.append(['*','*'])
				print "(MULTI, 0)"
			elif c == "/":
				tokens.append(['/','/'])
				print "(DIV,0)"
			elif c == "=":
				c = buf[cur+1]
				if c == "=":
					tokens.append(['==','eq'])
					cur += 1
					print "(EQL,0)"
				else:
					tokens.append(['=','='])
					print "(ASSIGN,0)"
			elif c == "<":
				c = buf[cur+1]
				if c == '=':
					cur = cur + 1
					print "(LE,0)"
					tokens.append(['<=','<='])
				else:
					tokens.append(['<','<'])
					print "(LT,0)"
			elif c == ">":
				c = buf[cur+1]
				if c == '=':
					cur = cur + 1
					print "(GE,0)"
					tokens.append(['>=','>='])
				else:
					tokens.append(['>','>'])
					print "(GT,0)"
			elif c == "(":
				tokens.append(['(','('])
				print "(LF_BRAC,0)"
			elif c == ")":
				tokens.append([')',')'])
				print "(RT_BRAC,0)"
			elif c == ",":
				tokens.append([',',','])
				print "(COMMA,0)"
			elif c == ";":
				tokens.append([';',';'])
				print "(SEMIC,0)"
			elif c == "[":
				tokens.append(['[','['])
				print "(LF_MB,0)"
			elif c == "]":
				tokens.append([']',']'])
				print "(RT_MB,0)"
			elif c == "{":
				tokens.append(['{','}'])
				print "(LF_BB,0)"
			elif c == "}":
				tokens.append(['}','}'])
				print "(RT_BB,0)"
			elif c == "%":
				tokens.append(['%','%'])
				print "(PERCENT,0)"
			elif c == "&":
				if buf[cur+1] == "&":
					cur += 1
					tokens.append(['&&','and'])
					print "(AND,0)"
				else:
					print "(ADDR,0)"
					tokens.append(['&','addr'])
			elif c == "|":
				if buf[cur+1] == "|":
					cur += 1
					print "(OR,0)"
					tokens.append(['||','or'])
				else:
					print "ERROR"
			elif c == "!":
				tokens.append(['!','not'])
				print "(NOT,0)"
			elif c == '"':
				cur = cur + 1
				c = buf[cur]
				while(c != '"'):
					cur = cur + 1
					c = buf[cur]
				tokens.append(['str',buf[start:cur+1]])
				print "(CONST,%s)" % buf[start:cur+1]
			else:
				print "ERROR"
		cur = cur + 1
	tokens.append(['#',-1])

def write_token():
	f = open('token.txt','w')
	for i in tokens:
		f.write('(%s,%s)\n' % (i[0],i[1]))
	f.close()

if __name__ == "__main__":
		if len(sys.argv) != 2:
			print "Usage: %s filename" % sys.argv[0]
			sys.exit(-1)
		get_token(sys.argv[1])
		write_token()

