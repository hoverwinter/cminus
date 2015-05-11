#!/usr/bin/env python
#encoding: utf-8

import json
table = []
sym = ["#","break","continue","else","float","for","if","int","return","void","while",
     "id","num","xiao","zhi","str","+","-","*","/","=","<",">","<=",">=","!=","(",")",",",";",
     "[","]","{","}","%","&&","||","!","++","==","&","printf","scanf","main","function",
     "S'","S","funtype","fun","fundecls","fundecl","decls","stmts","decl","type","ids","nums","stmt","expr",
     "asgn","funcs","func","funid","iter","slct","E","T","F","left","rel","inc","op","o","M1","M2","N1","N2","N3","N4",
     "N5","N6"]

def toJson():
	tmp = {}
	with open('LR(1).txt') as f:
		for line in f:
			res = line.strip().split(';')
			i = 0
			while i < 45:
				if int(res[i]) == 400:
					tmp[sym[i]] = 'err'
				elif int(res[i]) == 0:
					tmp[sym[i]] = 'acc'
				elif int(res[i]) > 0:
					tmp[sym[i]] = 'S'+res[i]
				else:
					tmp[sym[i]] = 'R'+res[i][1:]
				i = i + 1
			while i < 81:
				if int(res[i]) == 400:
					tmp[sym[i]] = 'err'
				else:
					tmp[sym[i]] = res[i]
				i = i + 1
			table.append(tmp.copy())
			tmp.clear()
	with open('table.json','w') as f:
		json.dump(table,f)




if __name__ == "__main__":
	toJson()
	print table