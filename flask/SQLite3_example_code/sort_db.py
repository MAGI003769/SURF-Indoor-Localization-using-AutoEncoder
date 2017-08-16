import sqlite3

def sort_db():
	conn = sqlite3.connect('fingerprints.db')
	cursor = conn.execute("SELECT id, BSSID, Frequency "
							"from COLLECTION ORDER BY Frequency DESC ")
	for row in cursor:
		print(row)
	conn.close()

sort_db()