import sqlite3

def HL_1():	 #GROUP BY
	conn = sqlite3.connect('fingerprints.db')
	cursor = conn.execute("SELECT Room, sum(Frequency)"
							"From COLLECTION GROUP BY Room")
	for row in cursor:
		print(row)

def HL_2(): #统计年龄超过30岁的员工的薪资
	conn = sqlite3.connect('fingerprints.db')
	cursor = conn.execute("SELECT ID,Frequency, sum(Level), Room "
							"FROM COLLECTION "
							"WHERE COLLECTION.Frequency>=2112 "
							"GROUP BY Room ORDER BY ID ")
	for row in cursor:
		print(row)

def HL_3(): #类似python的正则: sqlite 用 LIKE(% _) GLOB(* ?) 过滤
	conn = sqlite3.connect('fingerprints.db')
	cursor = conn.execute("SELECT ID, Frequency, Room "
							"FROM COLLECTION WHERE Room LIKE '3%'")
	for row in cursor:
		print(row)

def HL_4(): #取排序过后的TOP n 数据, 从第二个人 开始取
	conn = sqlite3.connect('fingerprints.db')
	cursor = conn.execute("SELECT * FROM COLLECTION "
							"ORDER BY Frequency DESC LIMIT 3 OFFSET 1")
	for row in cursor:
		print(row)

def HL_5(): #去除重复数据  有误
	conn = sqlite3.connect('fingerprints.db')
	cursor = conn.execute("SELECT DISTINCT count(Room) "
							"FROM COLLECTION "
							"GROUP BY Room ")
	for row in cursor:
		print(row)

HL_5()