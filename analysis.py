#!/usr/bin/env python
#encoding: utf-8

import re

V = None
T = None
P = None
S = None

class Item():
	def __init__(self,left,right,dot = -1,lookahead = '#'):
		if type(right) != type([]):
			print 'invaid parameter'
			self.right = []
		else:
			self.right = right
		self.left = left
		self.dot = dot
		self.lookahead = lookahead

	def go(self,X):
		if self.dot == -1:
			print '. Not found'
			return None
		if self.dot >= len(self.right):
			return None
		if self.right[self.dot] == X:
			b = Item(self.left,self.right,self.dot+1,self.lookahead)
			return b
		return None

	def __str__(self):
		s = ""
		for i in range(len(self.right)+1):
			if i == self.dot:
				s += '.'
			if i < len(self.right):
				s += self.right[i]
		return "[%s -> %s,%s]" % (self.left, s, self.lookahead)

	def __cmp__(self,other):
		return cmp(self.__str__(),other.__str__())

#
#	@function: get the grammar of high language
#
def getGrammar():
    global V, T, P, S
    a = raw_input('Please input the V:')
    V = set([x for x in a.strip().split(' ')])

    a = raw_input('Please input the T:')
    T = set([x for x in a.strip().split(' ')])

    P = []
    left = ''
    right = []
    a = raw_input('Please input the P:\n>>> ')
    while a != "":
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
        a = raw_input('>>> ')

    a = raw_input('Please input the S:')
    S = a

#
#	@input: X in (V U T)*
#	@return: set of first or None
#
def getFirst(X):
    first = set()
    if X in T:
        first.add(X)
        return first
    else:
        for item in P:
            if X == item.left:
                if item.right[0] in T:
                    first.add(item.right[0])
                else:
                    first = first.union(getFirst(item.right[0]))
    return first

#
#	@input: item and closure
#	@output: whether item is in closure
#
def item_in(item,I):
	if len(I) == 0:
		print 'invalid parameter'
		return False
	for i in I:
		if cmp(item,i)==0:
			return True
	return False

#
#	@output: whether two closure equals
#
def closure_eql(I,J):
	if len(I) == len(J) and len(J) == 0:
		return True
	if len(I) != len(J):
		return False
	flag = True
	for item in I:
		if not item_in(item,J):
			flag = False
	for item in J:
		if not item_in(item,I):
			flag = False
	return flag

#
#	@function: return the index of a closure in Item Set
#
def closure_index(Clr,ISet):
	if len(ISet) == 0 or len(Clr) == 0:
		print 'invalid parameter'
		return -1
	for tmp in range(len(ISet)):
		if closure_eql(Clr,ISet[tmp]):
			return tmp

#
#	@function: return the index of a product in P
#
def product_index(p):
	tmp = Item(p.left,p.right)
	for i in range(len(P)):
		if P[i] == tmp:
			return i
	return -1

#
#	@input: I in Items
#	@output: closure of I or None
#
def getClosure(I):
	res = []
	res.extend(I)
	if len(I) == 0:
		return None
	before = 0
	after = 1
	while before != after:
		before = after
		for item in res:
			if item.dot == -1:
				print 'invalid item of LR1'
				continue
			if item.dot >= len(item.right):
				continue
			tmp = item.right[item.dot]
			if tmp in V:
				for item2 in P:
					if item2.left == tmp:
						if item.dot+1 == len(item.right):
							# A->å.Xß ß第一个字符为空
							tmp_item = Item(item2.left,item2.right,0,item.lookahead)
							if not item_in(tmp_item,res):
								res.append(tmp_item)
						else:
							# A->å.Xß ß第一个字符first集
							for tmp2 in getFirst(item.right[item.dot+1]):
								tmp_item = Item(item2.left,item2.right,0,tmp2)
								if not item_in(tmp_item,res):
									res.append(tmp_item)
		after = len(res)
	return res

#
#	@input: I -> closure  and  X in (V U T)*
#	@output: closure of next state under X or None
#
def go(I,X):
	res = []
	if len(I) == 0:
		print 'invalid parameter'
		return None
	for item in I:
		tmp = item.go(X)
		if tmp != None:
			res.append(tmp)
	return getClosure(res)

#
#	@function: get all states
#
def getItemSetBranch():
	for tmp in P:
		if tmp.left == S:
			start_item = tmp
			break
	start_item.dot = 0
	start_item.lookahead = '#'

	closure_set = [getClosure([start_item])]
	for clr in closure_set:
		for X in V.union(T):
			I = go(clr,X)
			if I == None:
				continue
			flag = True
			for tmp in closure_set:
				if closure_eql(I,tmp):
					flag = False
					break
			if flag:
				closure_set.append(I)

	return closure_set

#
#	@function: show Item Set Branch
#
def showItemSetBranch():
	for i in getItemSetBranch():
		for j in i:
			print j
		print

#
#	@function: get Syntax Analysis Table
#
def makeTable():
	states = getItemSetBranch()
	table =[]
	for item in states:
		row = {}
		for tmp in T:
			for prod in item:
				if prod.lookahead == '#' and prod.left == S:
					row['#'] = 'acc'
				elif prod.lookahead == '#' and len(prod.right) == prod.dot:
					row['#'] = 'R'+str(product_index(prod))
				else:
					row['#'] = 'err'
				if prod.lookahead == tmp and len(prod.right) == prod.dot:
					row[tmp]='R'+str(product_index(prod))
				else:
					t = go(item,tmp)
					if t != None:
						row[tmp] = 'S'+str(closure_index(t,states))
					else:
						if row.get(tmp,None) == None:
							row[tmp] = 'err'	
		for tmp in V:
			t = go(item,tmp)
			if t == None:
				row[tmp]='err'
				continue
			row[tmp]=closure_index(t,states)
		table.append(row)
		print row
	return table

#
#	@function: LR analysis using table
#
def analysis():
	sentence = raw_input('Sentence to analysis:')
	print sentence

	table = makeTable()
	state = []
	vt = []
	state.append(0)
	vt.append('#')
	a = 0

	while True:
		s = state[-1]
		w = vt[-1]
		i = sentence[a]

		print 'State Stack: %s' % state
		print 'Symbol Stack: %s' % vt
		
		if table[s][i].find('S') != -1:
			vt.append(i)
			state.append(int(table[s][i][1:]))
			a += 1
			print 'shifting:'

		elif table[s][i].find('R') != -1:
			tmp = int(table[s][i][1:])
			for i in range(len(P[tmp].right)):
				state.pop()
				vt.pop()
			print 'reducing: '+ str(P[tmp])

			vt.append(P[tmp].left)
			state.append(table[state[-1]][P[tmp].left])
		elif table[s][i] == 'acc':
			print 'ACCEPT: analysis finished!'
			return 
		else:
			print 'sorry for ERROR!'
			return

if __name__ == "__main__":
	getGrammar()
	print 'Product:'
	for i in P:
		print i
	print
 	showItemSetBranch()
	analysis()
