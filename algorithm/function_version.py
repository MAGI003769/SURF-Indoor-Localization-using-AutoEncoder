import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt

session = tf.Session()

user_input = pd.read_csv("user_input.csv",header = 0)
user_input = np.asarray(user_input.ix[:, 0:520]).reshape([1, 520])
for j in range(520):
	if user_input[0][j] == 100:
		user_input[0][j] = -110
user_input = scale(user_input, axis=1)

test_dataset = pd.read_csv(".\\UJIndoorLoc\\validationData.csv",header = 0)
test_features = np.asarray(test_dataset.ix[:,0:520])
for i in range(test_features.shape[0]):
    for j in range(test_features.shape[1]):
        if test_features[i][j] == 100:
            test_features[i][j] = -110
test_features = scale(test_features, axis=1)
print('test_feature:', test_features.shape)
test_labels = np.asarray(test_dataset["BUILDINGID"].map(str) + test_dataset["FLOOR"].map(str))
test_labels = np.asarray(pd.get_dummies(test_labels))

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.0, shape = shape)
    return tf.Variable(initial)

n_input = 520 
n_classes = 13

n_hidden_1 = 256 
n_hidden_2 = 128 
n_hidden_3 = 64 

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

def encode(x):
    l1 = tf.nn.tanh(tf.add(tf.matmul(x,e_weights_h1),e_biases_h1))
    l2 = tf.nn.tanh(tf.add(tf.matmul(l1,e_weights_h2),e_biases_h2))
    l3 = tf.nn.tanh(tf.add(tf.matmul(l2,e_weights_h3),e_biases_h3))
    return l3
    
def decode(x):
    l1 = tf.nn.tanh(tf.add(tf.matmul(x,d_weights_h1),d_biases_h1))
    l2 = tf.nn.tanh(tf.add(tf.matmul(l1,d_weights_h2),d_biases_h2))
    l3 = tf.nn.tanh(tf.add(tf.matmul(l2,d_weights_h3),d_biases_h3))
    return l3

def dnn(x):
    l1 = tf.nn.relu(tf.add(tf.matmul(x,dnn_weights_h1),dnn_biases_h1))
    dropout = tf.nn.dropout(l1, 0.5)
    l2 = tf.nn.relu(tf.add(tf.matmul(l1,dnn_weights_h2),dnn_biases_h2))
    out = tf.nn.softmax(tf.add(tf.matmul(l2,dnn_weights_out),dnn_biases_out))
    return out

encoded = encode(X)
decoded = decode(encoded) 
y_ = dnn(encoded)

room = tf.argmax(y_, 1)

saver = tf.train.Saver()
saver.restore(session, ".\\trained_model\\trained_model.ckpt")

print(session.run(room, {X: user_input}))