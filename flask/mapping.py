# -*- coding:utf-8 -*-

from app import db, models
import csv

length = 200
 
PYTHONIOENCODING="UTF-8"  #set the utf-8 encode mode

def rawList():
	with open('mapping.csv', 'r', newline='') as csvfile: 
		#APsList = models.User.query.all() 
		reader = csv.reader(csvfile)
		APs = [row[0] for row in reader]
		
		APlength = len(APs)
		
		lists = [[0 for col in range(3)] for row in range(APlength)]
		
		row = 0
		for AP in APs:
			#dict_APs.update({AP:i})
			lists[row][0] = AP
			lists[row][1] = '-110'
			lists[row][2] = 'ee'
			row += 1
		
		return lists

def checkAP(list, AP):
	row = 0
	
	for row in range(0,length):
		if AP == list[row][0]:
			return row		
	return 'none'

	
list = rawList()
print(list)
print(checkAP(list, '4c:fa:ca:1f:41:40'))
#print(list)	