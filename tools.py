#!/usr/bin/env python
#encoding: utf-8

import re
S = set()
T = set()
def readFile():
	global T
	with open('grammar.txt') as f:
		for i in f:
			res = re.split('\s+',i.strip()[:-2])
			S.add(res[0])
			T = T.union(set(res[2:]))
	for item in S:
		if item in T:
			T.remove(item)

def writeFile():
	with open('vt.txt','w') as f:
		for item in S:
			f.write(item)
			f.write(' ')
		f.write('\n')
		for item in T:
			f.write(item)
			f.write(' ')

def ifProd():
	with open('tmp.txt','w') as f:
		i = 10
		while i < 80:
			f.write("if tmp == %d:\n\tpass\n" % i)
			i += 1

if __name__ == "__main__":
	# readFile()
	# print S
	# print T
	# writeFile()
	ifProd()