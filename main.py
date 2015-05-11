#!/usr/bin/python
#encoding= utf-8

import os
import json
from analysis import Item
import re
import copy
import sys

'''
2015-05-10
Author: Hover Winter
Copyright @ hoverwinter
Email: carpela@163.com
HIT License
'''
#调试模式
debug = False

P = [] #产生式
# 四元组表示为[
# 	{'no1':,'no2':,'no3':,'no4':,'order':},
#	{'no1':,'no2':,'no3':,'no4':,'order':}
# ]
fourtuple = [] 
semantic = []
# 函数标志
fnum = 1
# 四元组顺序
quad = 0
# 变量偏移
offset = 0
# 函数参数个数
pnum = 1
# 临时变量数目 
mid = 0
# 函数个数
symcount = 0
# 拉链回填
blists = []
btmp=[[],[]]
# 产生式
class Item():
	def __init__(self,left,right,dot = -1,lookahead = '#'):
		if type(right) != type([]):
			print 'invaid parameter'
			self.right = []
		else:
			self.right = right
		self.left = left

	def __str__(self):
		s = ""
		for i in self.right:
			s = s+i+' '
		return "[%s -> %s]" % (self.left, s)

# 处理声明
class Declare():
	def __init__(self,name="",dcrtype="",width=0,diem=0,len_a=0,variety=False):
		self.name = name
		self.type = dcrtype
		self.width = width
		self.diem = diem
		self.len_a = len_a
		self.variety = variety
		self.number = []
	def __str__(self):
		return '%s %s %s' %(self.name,self.type,self.width)

# 处理符号表
class Symbol():
	def __init__(self,name="",token="",length=0,dcrtype="",diem=0,len_a=0,addr=0,variety=False):
		self.name = name
		self.token = token
		self.length = length
		self.type = dcrtype #以下全是语义部分
		self.diem = diem 
		self.len_a = len_a
		self.addr = addr 
		self.variety = variety
		self.number = []
	def __str__(self):
		return '  [sym] %s %s addr:%s values:%s' % (self.name,self.type,self.addr,self.number)

# 处理函数符号表
class FuncSymbol():
	def __init__(self,fun_id="",fun_name="",length=0,num_param=0,location=0):
		self.symbol = [Symbol() for i in range(100)]
		self.fun_id = fun_id
		self.fun_name = fun_name
		self.length = length #参数和局部变量数
		self.num_param = num_param #语义修改
		self.location = location #语义修改

	def __str__(self):
		return "[fun:%s] %s: params:%d vars:%d addr:%s"  % (self.fun_id,self.fun_name,self.num_param,self.length,self.location)

#符号串 [[type,value],[type,value],...]
tokens = [] 
# 函数符号表
func_sym_tbl = [FuncSymbol() for i in range(10)]

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
	global tokens,debug,func_sym_tbl,symcount
	f = open(filename)
	buf = f.read()

	start = 0
	cur = 0

	flag = False
	sym = 0

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
			if debug:
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
				# 如果为main或者function处理符号表
				if key_tmp == 43:
					symcount = sym
					sym = 0
					flag=True
				if key_tmp == 44:
					sym+=1
					flag=True
				if debug:
					print "(%s,0)" % buf[start:cur].upper()
			else:
				if flag:
					if sym == 0:
						func_sym_tbl[sym].fun_name='main'
					else:
						func_sym_tbl[sym].fun_name=buf[start:cur]
					func_sym_tbl[sym].fun_id = sym
					flag = False
				else:
					ff = False
					for i in func_sym_tbl[sym].symbol:
						if i.name == buf[start:cur]:
							ff = True
							break
					if not ff:
						func_sym_tbl[sym].symbol[func_sym_tbl[sym].length].token=11
						func_sym_tbl[sym].symbol[func_sym_tbl[sym].length].length = cur-start+1
						func_sym_tbl[sym].symbol[func_sym_tbl[sym].length].name=buf[start:cur]
						func_sym_tbl[sym].length+=1

				tokens.append(['id',buf[start:cur]])
				if debug:
					print "(IDENT,%s)" % buf[start:cur]
			cur = cur - 1
		else:
			if c == "+":
				c = buf[cur+1]
				if c == '+':
					tokens.append(['++','++'])
					cur += 1
					if debug:
						print "(INC,-1)"
				else:
					tokens.append(['+','+'])
					if debug:
						print "(ADD,0)"
			elif c == "-":
				tokens.append(['-','-'])
				if debug:
					print "(MINUS, 0)"
			elif c == "*":
				tokens.append(['*','*'])
				if debug:
					print "(MULTI, 0)"
			elif c == "/":
				tokens.append(['/','/'])
				if debug:
					print "(DIV,0)"
			elif c == "=":
				c = buf[cur+1]
				if c == "=":
					tokens.append(['==','eq'])
					cur += 1
					if debug:
						print "(EQL,0)"
				else:
					tokens.append(['=','='])
					if debug:
						print "(ASSIGN,0)"
			elif c == "<":
				c = buf[cur+1]
				if c == '=':
					cur = cur + 1
					if debug:
						print "(LE,0)"
					tokens.append(['<=','<='])
				else:
					tokens.append(['<','<'])
					if debug:
						print "(LT,0)"
			elif c == ">":
				c = buf[cur+1]
				if c == '=':
					cur = cur + 1
					if debug:
						print "(GE,0)"
					tokens.append(['>=','>='])
				else:
					tokens.append(['>','>'])
					if debug:
						print "(GT,0)"
			elif c == "(":
				tokens.append(['(','('])
				if debug:
					print "(LF_BRAC,0)"
			elif c == ")":
				tokens.append([')',')'])
				if debug:
					print "(RT_BRAC,0)"
			elif c == ",":
				tokens.append([',',','])
				if debug:
					print "(COMMA,0)"
			elif c == ";":
				tokens.append([';',';'])
				if debug:
					print "(SEMIC,0)"
			elif c == "[":
				tokens.append(['[','['])
				if debug:
					print "(LF_MB,0)"
			elif c == "]":
				tokens.append([']',']'])
				if debug:
					print "(RT_MB,0)"
			elif c == "{":
				tokens.append(['{','}'])
				if debug:
					print "(LF_BB,0)"
			elif c == "}":
				tokens.append(['}','}'])
				if debug:
					print "(RT_BB,0)"
			elif c == "%":
				tokens.append(['%','%'])
				if debug:
					print "(PERCENT,0)"
			elif c == "&":
				if buf[cur+1] == "&":
					cur += 1
					tokens.append(['&&','and'])
					if debug:
						print "(AND,0)"
				else:
					if debug:
						print "(ADDR,0)"
					tokens.append(['&','addr'])
			elif c == "|":
				if buf[cur+1] == "|":
					cur += 1
					if debug:
						print "(OR,0)"
					tokens.append(['||','or'])
				else:
					print "ERROR"
			elif c == "!":
				tokens.append(['!','not'])
				if debug:
					print "(NOT,0)"
			elif c == '"':
				cur = cur + 1
				c = buf[cur]
				while(c != '"'):
					cur = cur + 1
					c = buf[cur]
				tokens.append(['str',buf[start:cur+1]])
				if debug:
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


def find_sym(fnum,name):
	for i in range(len(func_sym_tbl[fnum].symbol)):
		if func_sym_tbl[fnum].symbol[i].name == name:
			return i
	return -1

def parse():
	global P,pnum,fnum,offset,quad,semantic,fourtuple,func_sym_tbl,mid,symcount,blists,btmp,tokens
	global debug
	if len(tokens) == 0:
		get_token('source.c')
	# sentence = open('data.txt').read()
	left = ''
	right = []
	with open('grammar.txt') as f:
		for a in f:
			tmp = re.split('\s+',a.strip())
			for i in range(len(tmp)):
				if i == 1:
					continue
				if i == 0:
					left = tmp[i]
				else:
					right.append(tmp[i])
			P.append(Item(left,right))
			left = ''
			right = []
	if os.path.exists('table.json'):
		with open('table.json','r') as f:
			table = json.load(f)
	else:
		print 'LR(1) table not found!'

	# 初始化
	state = []
	vt = []
	state.append(0)
	vt.append('#')
	a = 0
	# sentence = sentence.strip().split(' ')
	# print sentence

	sym = {}
	dcr = Declare()
	dcrs = []
	var = []
	sn = []
	Q = []
	#以下用于拉链回填
	M1 =[]
	M2 =[]
	N1=[]
	N2=[]
	N3=[]
	N4=[]
	N5=[]
	sn=[]
	sntmp=[]
	n=[]
	stmp=[]
	N6=[]
	m1=0
	m2=0
	n1=0
	n2=0
	n3=0
	n4=0
	n5=0
	n6=0
	# 处理
	rt = [] #从后向前保存规约时右部文法的值
	if '-t' in sys.argv:
		wf = open('log.txt','w')
	while True:
		s = state[-1]
		w = vt[-1]
		ty = tokens[a][0]
		val = tokens[a][1]

		if debug:
			print 'State Stack: %s' % state
			print 'Symbol Stack: %s' % vt
			print a,tokens[a]

		if '-t' in sys.argv:
			wf.write('State Stack: %s\n' % state)
			wf.write('Symbol Stack: %s\n' % vt)
			wf.write(str(a)+' '+str(tokens[a])+'\n')

		if table[s][ty].find('S') != -1:
			vt.append(val)
			state.append(int(table[s][ty][1:]))
			a += 1
			if debug:
				print 'shifting:\n'
			if '-t' in sys.argv:
				wf.write('shifting:\n')

		elif table[s][ty].find('R') != -1:
			index = int(table[s][ty][1:])
			for i in range(len(P[index].right)):
				state.pop()
				rt.append(vt[-1])
				vt.pop()
			if '-t' in sys.argv:
				wf.write('reducing: %s' % str(P[index]))
			if debug:
				print 'reducing: '+ str(P[index])

			# 矫正fnum的值
			if fnum >symcount:
				fnum = 0
				func_sym_tbl[fnum].location = len(fourtuple)
			# S' -> S
			# S -> void main ( ) { decls stmts } 
			# S -> fun S
			# fun -> fun fun
			if 0<= index <=3: 
				pass
			# fun -> type  function id ( fundecls ) { decls stmts } 
			if index == 4:
				fnum += 1
				func_sym_tbl[fnum].location = len(fourtuple)
				pnum = 1
			# fundecls -> fundecls , fundecl 
			if index == 5:
				func_sym_tbl[fnum].num_param += 1
				for i in dcrs:
					b = find_sym(fnum,i.name)
					func_sym_tbl[fnum].symbol[b].len_a = i.len_a
					func_sym_tbl[fnum].symbol[b].type = i.type
					func_sym_tbl[fnum].symbol[b].variety = i.variety
					func_sym_tbl[fnum].symbol[b].diem = i.diem
					func_sym_tbl[fnum].symbol[b].addr = offset
					if i.type == 'float':
						if i.variety == False:
							offset += 8
						else:
							offset = offset+8*i.len_a
					if i.type == 'int':
						if i.variety == False:
							offset += 4
						else:
							offset = offset + 4*i.len_a

					func_sym_tbl[fnum].symbol[b].number = i.number[:]
				dcr.number[:] = []
				dcrs[:] = []
			# fundecls -> fundecl 
			if index == 6:
				func_sym_tbl[fnum].num_param += 1
			# fundecl -> type id
			if index == 7:
				tmp = copy.deepcopy(dcr)
				tmp.name = rt[0]
				tmp.diem = 0
				tmp.len_a = 0
				tmp.variety = False
				dcrs.append(tmp)
			# decls -> decls decl
			if index == 8:
				pass
			# decls -> decl
			if index == 9:
				pass
			# decl -> type ids ;
			if index == 10:
				for i in dcrs:
					b = find_sym(fnum,i.name)
					func_sym_tbl[fnum].symbol[b].len_a = i.len_a
					func_sym_tbl[fnum].symbol[b].type = i.type
					func_sym_tbl[fnum].symbol[b].variety = i.variety
					func_sym_tbl[fnum].symbol[b].diem = i.diem
					func_sym_tbl[fnum].symbol[b].addr = offset
					if i.type == 'float':
						if i.variety == False:
							offset += 8
						else:
							offset = offset+8*i.len_a
					if i.type == 'int':
						if i.variety == False:
							offset += 4
						else:
							offset = offset + 4*i.len_a

					func_sym_tbl[fnum].symbol[b].number = i.number[:]
				dcr.number[:] = []
				dcrs[:] = []
			# type -> float 
			if index == 11:
				dcr.type = 'float'
			# type -> int
			if index == 12:
				dcr.type = 'int'
			# funtype -> float
			if index == 13:
				pass
			# funtype -> int
			if index == 14:
				pass
			# ids -> ids , N6 id
			if index == 15:
				# print rt[0]
				var.append(rt[0])
				tmp = copy.deepcopy(dcr)
				tmp.name=rt[0]
				tmp.diem=0
				tmp.len_a=0
				tmp.variety=False
				dcrs.append(tmp)
				Q.append(rt[0])
			# ids -> id
			if index == 16:
				var.append(rt[0])
				tmp = copy.deepcopy(dcr)
				tmp.name=rt[0]
				tmp.diem=0
				tmp.len_a=0
				tmp.variety=False
				dcrs.append(tmp)
				Q.append(rt[0])
			# ids -> id [ num ] = { nums }
			if index == 17:
				tmp = copy.deepcopy(dcr)
				tmp.name=rt[7]
				tmp.diem=1
				tmp.len_a=int(rt[5])
				tmp.variety=True
				dcrs.append(tmp)
				q=rt[7]
				q+=rt[6]
				q+=str(rt[5])
				q+=rt[4]
				Q.append(q)
			# nums -> nums , num
			if index == 18:
				b=int(rt[0])
				dcr.number.append(b);
			# nums -> num
			if index == 19:
				b=int(rt[0])
				dcr.number.append(b);
			# nums -> xiao
			if index == 20:
				s=float(rt[0])
				dcr.number.append(s)
            # nums -> zhi
			if index == 21:
				pass
			# stmts -> stmts stmt
			if index == 22:
				if len(sn) != 0:
					for i in range(len(sn[-1])):
						fourtuple[sn[-1][i]]['no4']=str(quad)
					sn.pop()
            # stmts -> stmt 
			if index == 23:
				if len(sn) != 0:
					for i in range(len(sn[-1])):
						fourtuple[sn[-1][i]]['no4']=str(quad)
					sn.pop()
			# stmt -> return expr ;
			if index == 24:
				fourtuple.append({'no1':'ret','no2':'','no3':'','no4':semantic[-1],'order':quad})
				quad += 1
			# stmt -> asgn ;
			if index == 25:
				pass
			# stmt -> iter
			if index == 26:
				pass
			# stmt -> slct
			if index == 27:
				pass
			# stmt -> { stmts }
			if index == 28:
				pass
			#stmt -> continue
			if index == 29:
				pass
			#stmt -> break 
			if index == 30:
				pass
			#expr -> E
			if index == 31:
				pass
			# E -> E + T
			if index == 32:
				no1 = "+"
				no3 = semantic[-1]
				semantic.pop()
				no2 = semantic[-1]
				semantic.pop()
				no4 = "t"+str(mid)
				mid += 1
				order = quad
				quad += 1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				semantic.append(no4)
            # E -> E - T
			if index == 33:
				no1 = "-"
				no3 = semantic[-1]
				semantic.pop()
				no2 = semantic[-1]
				semantic.pop()
				no4 = "t"+str(mid)
				mid += 1
				order = quad
				quad += 1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				semantic.append(no4)
			# E -> T
			if index == 34:
				pass
			# T -> T * F
			if index == 35:
				no1 = "*"
				no3 = semantic[-1]
				semantic.pop()
				no2 = semantic[-1]
				semantic.pop()
				no4 = "t"+str(mid)
				mid += 1
				order = quad
				quad += 1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				semantic.append(no4)
			# T -> T / F
			if index == 36:
				no1 = "/"
				no3 = semantic[-1]
				semantic.pop()
				no2 = semantic[-1]
				semantic.pop()
				no4 = "t"+str(mid)
				mid += 1
				order = quad
				quad += 1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				semantic.append(no4)
			# T -> T % F
			if index == 37:
				no1 = "%"
				no3 = semantic[-1]
				semantic.pop()
				no2 = semantic[-1]
				semantic.pop()
				no4 = "t"+str(mid)
				mid += 1
				order = quad
				quad += 1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				semantic.append(no4)
			# T -> F
			if index == 38:
				pass
			# F -> ( E )
			if index == 39:
				pass
			# F -> num
			if index == 40:
				semantic.append(rt[0])
			# F -> xiao
			if index == 41:
				semantic.append(rt[0])
			# F -> zhi 
			if index == 42:
				pass
			# F -> id
			if index == 43:
				semantic.append(rt[0])
			# F -> id [ expr ]
			if index == 44:
				no1 = "*"
				no2 = semantic[-1]
				semantic.pop()
				u = 0
				while u < func_sym_tbl[fnum].length:
					if func_sym_tbl[fnum].symbol[u].name == rt[3]:
						break;
					u+=1
				if func_sym_tbl[fnum].symbol[u].type == 'int':
					no3 = '4'
				if func_sym_tbl[fnum].symbol[u].type == 'float':
					no3 = '8'
				no4 = "t"+str(mid)
				mid+=1 
				order = quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				semantic.append(no4)

				no1 = '=[]'
				no2 = rt[3]
				no3 = semantic[-1]
				semantic.pop()
				no4 = 't'+str(mid)
				mid+=1
				order = quad
				quad += 1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				semantic.append(no4)
			# asgn -> left = expr
			if index == 45:
				no1="="
				no2=semantic[-1]
				semantic.pop()
				no3=""
				no4=semantic[-1]
				semantic.pop()
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
			# asgn -> left = funid ( funcs )
			if index == 46:
				no1='call'
				no2=semantic[-1]
				no3=str(pnum)
				t=0
				tmp = ""
				while t<=symcount:
					if func_sym_tbl[t].fun_name == semantic[-1]:
						tmp = func_sym_tbl[t].location
						break
					t+=1
				no4 = tmp
				order = quad
				quad+=1
				semantic.pop()
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				no1='f='
				no2=semantic[-1]
				semantic.pop()
				no3=""
				no4=""
				order=quad
				quad+=1
				semantic.pop()
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
			# funid -> id
			if index == 47:
				semantic.append(rt[0])
			# funcs -> funcs , func
			if index == 48:
				pnum+=1
			# funcs -> func 
			if index == 49:
				pass
			# func -> id 
			if index == 50:
				no1="param"
				no2=""
				no3=""
				no4=rt[0]
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
			# func -> num
			if index == 51:
				no1="param"
				no2=""
				no3=""
				no4=rt[0]
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				pnum+=1
			# left -> id
			if index == 52:
				semantic.append(rt[0])
			# left -> id [ expr ] 
			if index == 53:
				no1 = "*"
				no2 = semantic[-1]
				semantic.pop()
				u = 0
				while u < func_sym_tbl[fnum].length:
					if func_sym_tbl[fnum].symbol[u].name == rt[3]:
						break;
					u+=1
				if func_sym_tbl[fnum].symbol[u].type == 'int':
					no3 = '4'
				if func_sym_tbl[fnum].symbol[u].type == 'float':
					no3 = '8'
				no4 = "t"+str(mid)
				mid+=1 
				order = quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				semantic.append(no4)

				no1 = '=[]'
				no2 = rt[3]
				no3 = semantic[-1]
				semantic.pop()
				no4 = 't'+str(mid)
				mid+=1
				order = quad
				quad += 1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				semantic.append(no4)
			# iter -> for ( asgn ; M1 rel ; N4 inc ) N2 stmt
			if index == 54:
				btmp = blists[-1]
				blists.pop()
				tmp = str(M2[-1])
				M2.pop()
				for i in range(len(btmp[1])):
					fourtuple[btmp[1][i]]['no4'] = tmp
				tmp = str(N4[-1])
				no1='j'
				no2=''
				no3=''
				no4=tmp
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})

				tmp=str(N4[-1])
				N4.pop()
				if(len(sn)!=0):
					for i in len(sn[-1]):
						fourtuple[sn[-1][i]]['no4']=tmp
					sn.pop()
				sntmp[:] = btmp[0]
				sn.append(sntmp)
			# iter -> while M1 ( rel ) M2 stmt 
			if index == 55:
				tmp = M1[-1]
				M1.pop()
				no1='j'
				no2=''
				no3=''
				no4=''
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				if len(sn)!=0:
					sntmp = sn[-1]
					sn.pop()
					for i in len(sntmp):
						fourtuple[sntmp[i]]['no4']=tmp
				tmp = M2[-1]
				M2.pop()
				for i in range(len(blists[-1][1])):
					fourtuple[blists[-1][1][i]]['no4']=tmp

				sntmp=blists[-1][0][:]
				blists.pop()
				sn.push(sntmp)
			# M1 -> 
			if index == 56:
				m1=quad
				M1.append(m1)
			# M2 ->
			if index == 57:
				m2=quad
				M2.append(m2)
			# N1 ->
			if index == 58:
				stmp.append(quad)
				n.append(stmp)
				no1='j'
				no2=''
				no3=''
				no4=''
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
			# N2 -> 
			if index == 59:
				no1='j'
				no2=''
				no3=''
				no4=str(M1[-1])
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				m2=quad
				M2.append(m2)
			# N3 -> 
			if index == 60:
				n3=quad
				N3.append(n3)
			# N4 -> 
			if index == 61:
				n4=quad
				N4.append(n4)
			# N5 -> 
			if index == 62:
				Q[:]=[]
			# N6 ->
			if index == 63:
				pass
			# rel -> expr op expr
			if index == 64:
				btmp[0][:]=[]
				btmp[1][:]=[]
				no3=semantic[-1]
				semantic.pop()
				no1='j'
				no1+=str(semantic[-1])
				semantic.pop()
				no2=semantic[-1]
				semantic.pop()
				no4=''
				btmp[1].append(quad)
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				no1='j'
				no2=''
				no3=''
				no4=''
				order=quad
				btmp[0].append(quad)
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				blists.append(btmp)
				quad+=1
			# rel -> ! rel 
			if index == 65:
				btmp[0][:]=[]
				btmp[1][:]=[]
				btmp=blists[-1]
				blists[-1][0]=btmp[0][:]
				blists[-1][1]=btmp[1][:]
			# rel -> rel o N3 rel 
			if index == 66:
				btmp[0][:]=[]
				btmp[1][:]=[]
				if semantic[-1]=='||':
					btmp=blists[-1]
					blists.pop()
					N3.pop()
					for i in range(len(blists[-1][0])):
						fourtuple[blists[-1][0][i]]['no4']=tmp
					for i in range(len(blists[-1][1])):
						fourtuple[blists[-1][1][i]]['no4']=tmp 
					blists.pop()
					blists.append(btmp)
				if semantic[-1]=='&&':
					btmp=blists[-1]
					blists.pop()
					tmp = str(N3[-1])
					N3.pop()
					for i in range(len(blists[-1][0])):
						fourtuple[blists[-1][0][i]]['no4']=tmp
					for i in range(len(blists[-1][1])):
						btmp[0].append(blists[-1][0][i])
					blists.pop()
					blists.append([btmp[0][:],btmp[1][:]])
			# op -> <
			if index == 67:
				semantic.append(rt[0])
			# op -> > 
			if index == 68:
				semantic.append(rt[0])
			# op -> <=
			if index == 69:
				semantic.append(rt[0])
			# op -> >= 
			if index == 70:
				semantic.append(rt[0])
			# op -> == 
			if index == 71:
				semantic.append(rt[0])
			# op -> !=
			if index == 72:
				semantic.append(rt[0])
			# o -> && 
			if index == 73:
				semantic.append(rt[0])
			# o -> ||
			if index == 74:
				semantic.append(rt[0])
			# inc -> left ++
			if index == 75:
				no1="++";
				no2=semantic[-1];
				no3="";
				no4=semantic[-1];
				semantic.pop();
				order=quad;
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
			# slct -> if ( rel ) M1 stmt N1 else M2 stmt 
			if index == 76:
				btmp=blists[-1]
				blists.pop()
				tmp=str(M1[-1])
				M1.pop()
				for i in range(len(btmp[1])):
					fourtuple[btmp[1][i]]['no4']=tmp
				tmp = str(M2[-1])
				M2.pop()
				for i in range(len(btmp[0])):
					fourtuple[btmp[0][i]]['no4']=tmp
				if len(sn)==0:
					sn.append(n[-1])
					n.pop()
				else:
					sntmp=sn[-1]
					sn.pop()
					for i in range(len(n[-1])):
						sntmp.append(n[-1][i])
					n.pop()
					if len(sn)==0:
						sn.append(sntmp)
					else:
						for i in range(len(sn[-1])):
							sntmp.append(sn[-1][i])
						sn.pop()
						sn.push(sntmp)
			# stmt -> printf ( str ) ;
			if index == 77:
				no1="param"
				no2=""
				no3=""
				no4=rt[2]
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				no1="call"
				no2="printf"
				no3="1"
				no4=""
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
			# stmt -> printf ( str , N5 ids ) ;
			if index == 78:
				no1="param"
				no2=""
				no3=""
				no4=rt[5]
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				for i in range(len(Q)):
					no1='param'
					no2=''
					no3=''
					no4=Q[i]
					order=quad
					quad+=1
					fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				no1="call"
				no2="printf"
				tmp = str(len(Q)+1)
				no3=tmp;
				no4="";
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
			# stmt -> scanf ( str , & id ) ;
			if index == 79:
				no1="param"
				no2=""
				no3=""
				no4=rt[5]
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				no1="param";
				no2="";
				no3="";
				no4=rt[2]
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})
				no1="call";
				no2="scanf";
				no3="2";
				no4="";
				order=quad
				quad+=1
				fourtuple.append({'no1':no1,'no2':no2,'no3':no3,'no4':no4,'order':order})

			vt.append(P[index].left)
			state.append(int(table[state[-1]][P[index].left]))
			if '-t' in sys.argv:
				wf.write(str(rt)+'\n')
			rt[:] = []
		elif table[s][ty] == 'acc':
			if '-t' in sys.argv:
				wf.close()
			if '-s' in sys.argv:
				write_symbol()
			print 'ACCEPT: syntax analysis and code generating finished!'
			return
		else:
			print 'FAILURE: sorry for ERROR!'
			return

def write_tuple():
	wf=open('result.txt','w')
	for item in fourtuple:
		wf.write('%d(%s,%s,%s,%s)\n'%(item['order'],item['no1'],item['no2'],item['no3'],item['no4']))

def write_symbol():
	wf=open('symbol.txt','w')
	for i in range(symcount+1):
		item = func_sym_tbl[i]
		wf.write('%s\n'%item)
		if debug:
			print item
		for j in range(item.length):
			wf.write('%s\n'%item.symbol[j])
			if debug:
				print item.symbol[j]

def usage():
	print '''%s [-d] [-t] [-l] [-s] srcfile
output four tuple in [result.txt]
-d : output debug information
-t : save tokens in file [token.txt]
-l : save parse processing in file [log.txt]
-s : save symbol table in file [symbol.txt]''' % sys.argv[0]

if __name__ == "__main__":
	if 2<= len(sys.argv) <=6:
		get_token(sys.argv[-1])
		if '-t' in sys.argv:
			write_token()
		parse()
		write_tuple()
	else:
		usage()





