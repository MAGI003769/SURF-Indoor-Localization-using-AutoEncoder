import sqlite3

def insert_db():
	conn = sqlite3.connect('fingerprints.db')
	conn.execute("INSERT INTO COLLECTION (ID,Building,Room,Location_x,Location_y,SSID,BSSID,Frequency,Level) "
				 "VALUES(7,'EE','321',1,1,'A','2f:3d:4a',2113,-110)")
	conn.commit()
	conn.close()

insert_db()
