# coding: utf-8
from flask import Flask, request
from app import db, models
import csv
import os #to get current path
import importlib
import sqlite3 #about database 

from model import *

#algorithm part 
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt

PYTHONIOENCODING="UTF-8"  #set the utf-8 encode mode

	
# create the application object
app = Flask(__name__)


#Add RSS info into database whose name is app.db
def addAPs(list):
	for row in range(0,200):
		u = models.User(Room = list[row][2], BSSID = list[row][0],  Level = list[row][1])
		db.session.add(u)
	db.session.commit()

#Show all RSS info from database	
def showAPs(num):	
	ap = models.User.query.get(num)
	print(ap.Building, ap.Room, ap.Location_x, ap.BSSID, ap.Level)

	
# Write all info in DB into a csv file, without SSID stored, encode mode is UTF-8 (as some SSID contains chinese characters)
def addAllCSV():    #whole database	
	with open('APs.csv', 'w', newline='') as csvfile: 
		if not os.path.getsize('./APs.csv'): 
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
			spamwriter.writerow([ 'Room', 'BSSID',  'Level'])
		
		users = models.User.query.all()
		
		for u in users:
			data = ([
			 u.Room, u.BSSID, u.Level
			])
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
			spamwriter.writerow(data)
			
#add one time's scanner result			
def addCSV(Building, Room, Location_x, Location_y, BSSID, Frequency, Level, Model, Time):    
	with open('userinput.csv', 'a', newline='') as csvfile: 		
		if not os.path.getsize('./userinput.csv'): 
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
			spamwriter.writerow(['Building', 'Room', 'Location_x', 'Location_y', 'BSSID', 'Frequency', 'Level', 'Model', 'Time'])
		
		data = ([
		Building, Room, Location_x, Location_y, BSSID, Frequency, Level, Model, Time
		])

		spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
		spamwriter.writerow(data)
			
def deleteDB():
	users = models.User.query.all()
	
	for u in users:
		db.session.delete(u)
		
	db.session.commit()


def initializeTempList():
	with open('mapping.csv', 'r', newline='') as csvfile:  
		reader = csv.reader(csvfile)
		APs = [row[0] for row in reader]
		APlength = len(APs)
		lists = [[0 for col in range(5)] for row in range(APlength)]
		row = 0
		for AP in APs:
			lists[row][0] = AP
			lists[row][1] = '-110'
			lists[row][2] = 'none'
			lists[row][3] = 'none'
			lists[row][4] = 'none'
			row += 1

	with open('tempList.csv', 'w', newline='') as csvfile: 
		spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
		spamwriter.writerow([ 'Room', 'BSSID',  'Level', 'Model', 'Time'])
		for i in range(0,200): 
			data = ([
			lists[i][0], lists[i][1], lists[i][2], lists[i][3], lists[i][4]
			])
			spamwriter.writerow(data)
		
#Check if the input AP's BSSID is in the mapping.csv, which contains 200 APs
def checkAP(list, AP):
	row = 0
	
	for row in range(0,200):
		if AP == list[row][0]:
			return row      
	return 'none'           

def tempList(BSSID, Level, Room, Model, Time): 
	with open('tempList.csv', 'r', newline='') as csvfile: 
		reader = csv.reader(csvfile)
		RSS = [row for row in reader]
		#print(RSS,RSS[0][0])
		for row in range(1,201):        
			if  RSS[row][0] == BSSID :
				RSS[row][1] = Level     
				RSS[row][2] = Room
				RSS[row][3] = Model
				RSS[row][4] = Time
				
				with open('tempList.csv', 'w', newline='') as csvfile: 
					spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
					spamwriter.writerow(['BSSID', 'Level', 'Room', 'Model', 'Time'])             
					for i in range(1,201):
						data = ([
						RSS[i][0], RSS[i][1], RSS[i][2], RSS[i][3], RSS[i][4]
						])
						spamwriter.writerow(data)
				break
	
def isEmpty():
	with open('xxx.csv', 'a+', newline='') as csvfile:  #Check is tempList is empty	
		if not os.path.getsize('./xxx.csv'):        #file not established
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
			spamwriter.writerow(['BSSID',  'Level', 'Room', 'Model', 'Time'])
	
	with open('mapping.csv', 'r', newline='') as csvfile:  
		reader = csv.reader(csvfile)
		APs = [row[0] for row in reader]
		APlength = len(APs)
		lists = [[0 for col in range(5)] for row in range(APlength)]
		row = 0
		for AP in APs:
			lists[row][0] = AP
			lists[row][1] = '-110'
			lists[row][2] = 'none'
			lists[row][3] = 'none'
			lists[row][4] = 'none'
			row += 1
	
	with open('tempList.csv', 'a+', newline='') as csvfile:     #Check is tempList is empty	
		if not os.path.getsize('./tempList.csv'):       #file is empty
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
			spamwriter.writerow(['BSSID',  'Level', 'Room', 'Model', 'Time'])
			for i in range(0,200): 
				data = ([
				 lists[i][0], lists[i][1], lists[i][2], lists[i][3], lists[i][4]
				])
				spamwriter.writerow(data)
	
def refreshCSV(Room,Model,Time):
	with open('tempList.csv', 'r', newline='') as csvfile: 
		reader = csv.reader(csvfile)
		RSS = [row for row in reader]
		
		with open('tempList.csv', 'w', newline='') as csvfile: 
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
			spamwriter.writerow(['BSSID',  'Level', 'Room', 'Model', 'Time'])
			for row in range(1,201):
				RSS[row][2] = Room
				RSS[row][3] = Model
				RSS[row][4] = Time

				room = ([
					RSS[row][0], RSS[row][1], RSS[row][2], RSS[row][3], RSS[row][4]
					])
				spamwriter.writerow(room)
		
		with open('xxx.csv', 'a', newline='') as csvfile: 
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
								
			for i in range(1,201):
				data = ([
				RSS[i][0], RSS[i][1], RSS[i][2], RSS[i][3], RSS[i][4]
				])
				spamwriter.writerow(data)
		
		with open('oneTime.csv', 'a', newline='') as csvfile: 			
			if not os.path.getsize('./oneTime.csv'):        #file is empty
				spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
				spamwriter.writerow(['BSSID',  'Level', 'Room', 'Model', 'Time'])    
			
			for i in range(1,201):
				data = ([
				RSS[i][0], RSS[i][1], RSS[i][2], RSS[i][3], RSS[i][4]
				])
				spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
				spamwriter.writerow(data)
				
#add to database, using sqlite3
def addToDB():
	with open('tempList.csv', 'r', newline='') as csvfile: 
		reader = csv.reader(csvfile)
		RSS = [row for row in reader]

	conn = sqlite3.connect('fingerprints.db')
	for i in range(1,201):

		conn.execute("INSERT INTO COLLECTION (ID,BSSID,Level,Room, Model, Time) "
				 	"VALUES(null,'"+RSS[i][0]+"','"+RSS[i][1]+"','"+RSS[i][2]+"','"+RSS[i][3]+"','"+RSS[i][4]+"')")
	conn.commit()
	conn.close()

@app.route('/', methods=['POST'])
def post():
	isEmpty()

	Building = request.form['Building']
	Room = request.form['Room']
	Location_x = request.form['Location_x']
	Location_y = request.form['Location_y']
	SSID = request.form['SSID']
	BSSID = request.form['BSSID']
	Frequency = request.form['Frequency']
	Level = request.form['Level']
	Model = request.form['Model']
	Time = request.form['Time']

	Done = request.form['Done']
	
	tempList(BSSID, Level, Room, Model, Time)
	
	if Done == 'YES':
		refreshCSV(Room,Model,Time)	
		addToDB()

		initializeTempList()
		print('YES')
	else:
		print('NO')
	#addAPs(list)
	#addAllCSV()
	
	#addAPs(Building, Room, Location_x, Location_y, SSID,BSSID, Frequency, Level)
	
	#addCSV(Building, Room, Location_x, Location_y, BSSID, Frequency, Level)


	#print('Building:'Building, 'Room:'Room,'Location_x:'Location_x, 'Location_y:'Location_y, 'SSID:'SSID, 'BSSID:'BSSID, 'Frequency:'Frequency, 'Level:'Level, 'Down?:'Down)
	#print ("Building: %s, Room: %s, Location_x: %s, Location_y: %s, SSID: %s, BSSID: %s, Frequency: %s, Level: %s, Down?: %s" % (Building, Room, Location_x, Location_y, SSID, BSSID, Frequency, Level, Down))

	return 'OK.'
if __name__ == "__main__":
	app.run(host='192.168.43.222', debug=True)
	#app.run(host='192.168.43.222', debug=True)


