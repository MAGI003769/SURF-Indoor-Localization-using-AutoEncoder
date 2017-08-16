# coding: utf-8
from flask import Flask, request
from app import db, models
import csv
import os #to get current path
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import importlib

from model import *

#algorithm part 
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt

PYTHONIOENCODING="UTF-8"  #set the utf-8 encode mode

room_dic = {'0': 'the front of elevators', '1': 'Male Toilet', '2': 'Southern space', '3': 'Northern Space', '4': 'EE411', '5': 'EE405', '6': 'EE420'}
	
# create the application object
app = Flask(__name__)

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.0, shape = shape)
    return tf.Variable(initial)

def encode(x, e_weights_h1, e_weights_h2, e_weights_h3, e_biases_h1, e_biases_h2, e_biases_h3):
    l1 = tf.nn.tanh(tf.add(tf.matmul(x,e_weights_h1),e_biases_h1))
    l2 = tf.nn.tanh(tf.add(tf.matmul(l1,e_weights_h2),e_biases_h2))
    l3 = tf.nn.tanh(tf.add(tf.matmul(l2,e_weights_h3),e_biases_h3))
    return l3
    
def decode(x, d_weights_h1, d_weights_h2, d_weights_h3, d_biases_h1, d_biases_h2, d_biases_h3):
    l1 = tf.nn.tanh(tf.add(tf.matmul(x,d_weights_h1),d_biases_h1))
    l2 = tf.nn.tanh(tf.add(tf.matmul(l1,d_weights_h2),d_biases_h2))
    l3 = tf.nn.tanh(tf.add(tf.matmul(l2,d_weights_h3),d_biases_h3))
    return l3

def dnn(x, dnn_weights_h1, dnn_weights_h2, dnn_weights_out, dnn_biases_h1, dnn_biases_h2, dnn_biases_out):
    l1 = tf.nn.relu(tf.add(tf.matmul(x,dnn_weights_h1),dnn_biases_h1))
    #dropout = tf.nn.dropout(l1, 0.5)
    l2 = tf.nn.relu(tf.add(tf.matmul(l1,dnn_weights_h2),dnn_biases_h2))
    out = tf.nn.softmax(tf.add(tf.matmul(l2,dnn_weights_out),dnn_biases_out))
    return out

def run_model(user_input):
	with tf.Graph().as_default() as g:
		n_input = 200
		n_classes = 7

		n_hidden_1 = 128
		n_hidden_2 = 64 
		n_hidden_3 = 32 

		learning_rate = 0.01
		training_epochs = 20
		batch_size = 10
		# --------------------- Encoder Variables --------------- #

		X = tf.placeholder(tf.float32, shape=[None,n_input])
		Y = tf.placeholder(tf.float32,[None,n_classes])

		# --------------------- Encoder Variables --------------- #
		
		e_weights_h1 = weight_variable([n_input, n_hidden_1])
		e_biases_h1 = bias_variable([n_hidden_1])

		e_weights_h2 = weight_variable([n_hidden_1, n_hidden_2])
		e_biases_h2 = bias_variable([n_hidden_2])

		e_weights_h3 = weight_variable([n_hidden_2, n_hidden_3])
		e_biases_h3 = bias_variable([n_hidden_3])

		# --------------------- Decoder Variables --------------- #
		
		#d_weights_h1 = weight_variable([n_hidden_3, n_hidden_2])
		d_weights_h1 = tf.transpose(e_weights_h3)
		d_biases_h1 = bias_variable([n_hidden_2])

		#d_weights_h2 = weight_variable([n_hidden_2, n_hidden_1])
		d_weights_h2 = tf.transpose(e_weights_h2)
		d_biases_h2 = bias_variable([n_hidden_1])

		#d_weights_h3 = weight_variable([n_hidden_1, n_input])
		d_weights_h3 = tf.transpose(e_weights_h1)
		d_biases_h3 = bias_variable([n_input])

		# --------------------- DNN Variables ------------------ #

		dnn_weights_h1 = weight_variable([n_hidden_3, n_hidden_2])
		dnn_biases_h1 = bias_variable([n_hidden_2])

		dnn_weights_h2 = weight_variable([n_hidden_2, n_hidden_2])
		dnn_biases_h2 = bias_variable([n_hidden_2])

		dnn_weights_out = weight_variable([n_hidden_2, n_classes])
		dnn_biases_out = bias_variable([n_classes])
		
		
		init_op = tf.global_variables_initializer()
		encoded = encode(X, e_weights_h1, e_weights_h2, e_weights_h3, e_biases_h1, e_biases_h2, e_biases_h3)
		decoded = decode(encoded, d_weights_h1, d_weights_h2, d_weights_h3, d_biases_h1, d_biases_h2, d_biases_h3) 
		y_ = dnn(encoded, dnn_weights_h1, dnn_weights_h2, dnn_weights_out, dnn_biases_h1, dnn_biases_h2, dnn_biases_out)
		room = tf.argmax(y_, 1)
		
		#saver = tf.train.Saver()	
		
	with tf.Session(graph=g) as session:
		session.run(init_op)
		saver = tf.train.Saver()
		saver.restore(session, ".\\trained_model\\trained_model.ckpt")
		#print(session.run(y_, {X: user_input}))
		#print(session.run(room, {X: user_input}))
		return session.run(room, {X: user_input})


#Add apps info in database
def addAPs(list):
	for row in range(0,200):
		u = models.User(Room = list[row][2], BSSID = list[row][0],  Level = list[row][1])
		db.session.add(u)
	db.session.commit()
		
def showAPs(num):
	ap = models.User.query.get(num)
	print(ap.Building, ap.Room, ap.Location_x, ap.BSSID, ap.Level)
	
# without SSID stored, encode mode is UTF-8
def addAllCSV():    #whole database
	#csvfile = open('userinput.csv', 'w')   #use file() rather than open() in python2.7
	#Write mode 'a': write after...  ‘w'：clear all and write
	
	with open('APs.csv', 'w', newline='') as csvfile: 	
		if not os.path.getsize('./APs.csv'): 
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
			spamwriter.writerow([ 'Room', 'BSSID',  'Level', 'Model', 'Time'])
		
		users = models.User.query.all()
		
		for u in users:
			data = ([
			 u.Room, u.BSSID, u.Level
			])
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
			spamwriter.writerow(data)
			
def addCSV(Building, Room, Location_x, Location_y, BSSID, Frequency, Level, Model, Time):    #add one time's scanner result
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
		

def checkAP(list, AP):  #check if the AP exist in AP list or not
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
		'''
		with open('xxx.csv', 'a', newline='') as csvfile: 
			spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
								
			for i in range(0,200):
				data = ([
				RSS[i][0], RSS[i][1], RSS[i][2]
				])
				spamwriter.writerow(data)
		
		with open('oneTime.csv', 'a', newline='') as csvfile: 
			
			if not os.path.getsize('./oneTime.csv'):        #file is empty
				spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
				spamwriter.writerow(['BSSID',  'Level', 'Room'])    
			
			for i in range(0,200):
				data = ([
				RSS[i][0], RSS[i][1], RSS[i][2]
				])
				spamwriter.writerow(data)
				'''
	
@app.route('/', methods=['POST'])
def post():
	isEmpty()
	#lists = rawList()
	#isTempListEmpty()
	
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
	
	#print(Level, '    ', SSID, BSSID, Down)
	
	if(Done == 'YES'):
		refreshCSV(Room,Model,Time)
		
		user_input = pd.read_csv("tempList.csv",header = 0)
		user_input = np.asarray(user_input.ix[0:200, 1]).reshape([1, 200])
		user_input = scale(user_input, axis=1)
		location = run_model(user_input)
		
		#print('Location:', type(location))
		
		initializeTempList()
		
		print('\n=====================================================\n')
		print('\tYou are now at ', room_dic[str(location[0])])
		print('\n=====================================================\n')
		
		return str(location[0])
	#addAPs(list)
	#addAllCSV()
	#addAPs(Building, Room, Location_x, Location_y, SSID,BSSID, Frequency, Level)
	
	#addCSV(Building, Room, Location_x, Location_y, BSSID, Frequency, Level)
	#print('Building:'Building, 'Room:'Room,'Location_x:'Location_x, 'Location_y:'Location_y, 'SSID:'SSID, 'BSSID:'BSSID, 'Frequency:'Frequency, 'Level:'Level, 'Down?:'Down)
	#print ("Building: %s, Room: %s, Location_x: %s, Location_y: %s, SSID: %s, BSSID: %s, Frequency: %s, Level: %s, Down?: %s" % (Building, Room, Location_x, Location_y, SSID, BSSID, Frequency, Level, Down))

	return '[-1]'
if __name__ == "__main__":
	#app.run(host='0.0.0.0', debug=False)
	#app.run(host='192.168.43.202', debug=True)
	app.run(host='10.8.222.33', debug=True)
	


