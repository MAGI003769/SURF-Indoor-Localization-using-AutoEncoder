import sqlite3

def create_db():
	conn = sqlite3.connect('fingerprints.db')
	#no matter the table is exist or not exist, just del it
	#conn.execute("DROP TABLE COLLECTION; ")

	conn.execute('''CREATE TABLE IF NOT EXISTS COLLECTION
		(ID 		  INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT,
		Room          TEXT      NOT NULL,
		BSSID         TEXT      NOT NULL,
		Level         INT       NOT NULL,
		Model         TEXT      NOT NULL,
		Time          TEXT      NOT NULL);''')		

	conn.execute("INSERT INTO COLLECTION (ID,Room,BSSID,Level, Model, Time) "
				 "VALUES(null,'EE','420',11,'AAA','AA')")

	conn.execute("INSERT INTO COLLECTION (ID,Room,BSSID,Level, Model, Time) "
				 "VALUES(null,'EE','420',11,'AAA','AA')")

	conn.commit()
	conn.close()

create_db()