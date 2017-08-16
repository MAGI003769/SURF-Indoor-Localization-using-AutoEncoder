import sqlite3

def select_db():
	conn = sqlite3.connect('fingerprints.db')
	cursor = conn.execute("SELECT Frequency,Location_x from COLLECTION "
							"WHERE Frequency>=2000 and Location_x > 0")
	for row in cursor:
		print(row)
	conn.close()
	
select_db()