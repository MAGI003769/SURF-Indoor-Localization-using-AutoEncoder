import sqlite3

def update_db():
	conn = sqlite3.connect('fingerprints.db')
	conn.execute("UPDATE COLLECTION set Frequency = 2222 WHERE ID=2");
	conn.commit()
	conn.close()

update_db()