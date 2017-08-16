import sqlite3

def read_db():
	conn = sqlite3.connect('fingerprints.db')
	cursor = conn.execute("SELECT * from COLLECTION")
	for row in cursor:
		print("\nID = ", row[0])
		print("Building = ", row[1])
		print("Room = ", row[2])
		print("Location_x = ", row[3])
		print("Location_y = ", row[4])
		print("SSID = ", row[5])
		print("BSSID = ", row[6])
		print("Frequency = ", row[7])
		print("Level = ", row[8])
	conn.close()
read_db()