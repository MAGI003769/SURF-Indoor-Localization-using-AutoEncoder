import sqlite3

#删除表所有 DELETE FROM TABLE_NAME

def del_db():
	conn = sqlite3.connect('fingerprints.db')
	conn.execute("DELETE from COLLECTION where ID=2")
	conn.commit()

	cursor = conn.execute("SELECT * from COLLECTION")
	for row in cursor:
		print(row)
	conn.close()

del_db()