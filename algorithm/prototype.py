import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt

dataset = pd.read_csv(".\\UJIndoorLoc\\trainingData.csv",header = 0)
features = np.asarray(dataset.ix[:,0:520])
for i in range(features.shape[0]):
    for j in range(features.shape[1]):
        if features[i][j] == 100:
            features[i][j] = -110
features = scale(features, axis=1)
labels = np.asarray(dataset["BUILDINGID"].map(str) + dataset["FLOOR"].map(str))
labels = np.asarray(pd.get_dummies(labels))

train_val_split = np.random.rand(len(features)) < 0.90
train_x = features[train_val_split]
train_y = labels[train_val_split]
val_x = features[~train_val_split]
val_y = labels[~train_val_split]

test_dataset = pd.read_csv(".\\UJIndoorLoc\\validationData.csv",header = 0)
test_features = np.asarray(np.asarray(test_dataset.ix[:,0:520]))
for i in range(test_features.shape[0]):
    for j in range(test_features.shape[1]):
        if test_features[i][j] == 100:
            test_features[i][j] = -110
test_features = scale(test_features, axis=1)
test_labels = np.asarray(test_dataset["BUILDINGID"].map(str) + test_dataset["FLOOR"].map(str))
test_labels = np.asarray(pd.get_dummies(test_labels))

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.0, shape = shape)
    return tf.Variable(initial)

n_input = 520 
n_hidden_1 = 256 
n_hidden_2 = 128 
n_hidden_3 = 64 

n_classes = labels.shape[1]

learning_rate = 0.01
training_epochs = 20
batch_size = 10

total_batches = dataset.shape[0] // batch_size

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
    l3 = tf.nn.sigmoid(tf.add(tf.matmul(l2,d_weights_h3),d_biases_h3))
    return l3

def dnn(x):
    l1 = tf.nn.relu(tf.add(tf.matmul(x,dnn_weights_h1),dnn_biases_h1))
    #dropout = tf.nn.dropout(l1, 0.5)
    l2 = tf.nn.relu(tf.add(tf.matmul(l1,dnn_weights_h2),dnn_biases_h2))
    out = tf.nn.softmax(tf.add(tf.matmul(l2,dnn_weights_out),dnn_biases_out))
    return out

encoded = encode(X)
decoded = decode(encoded) 
y_ = dnn(encoded)

#us_cost_function = tf.reduce_mean(tf.pow(X - decoded, 2))
us_cost_function = tf.losses.mean_squared_error(decoded, X)
s_cost_function = -tf.reduce_sum(Y * tf.log(y_))
us_optimizer = tf.train.AdamOptimizer(learning_rate/10).minimize(us_cost_function)
s_optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(s_cost_function)
#us_optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(us_cost_function)
#s_optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(s_cost_function)

correct_prediction = tf.equal(tf.argmax(y_,1), tf.argmax(Y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# ------------------------- run the model --------------------------- #

with tf.Session() as session:
    tf.global_variables_initializer().run()
    
    # ------------ 1. Training Autoencoders - Unsupervised Learning ----------- #
    plot_loss = []
    plot_epoch = []
    for epoch in range(training_epochs):
        epoch_costs = np.empty(0)
        for b in range(total_batches):
            offset = (b * batch_size) % (features.shape[0] - batch_size)
            batch_x = features[offset:(offset + batch_size), :]
            _, c = session.run([us_optimizer, us_cost_function],feed_dict={X: batch_x})
            epoch_costs = np.append(epoch_costs,c)
        print ("Epoch: ",epoch," Loss: ",np.mean(epoch_costs))
        plot_epoch.append(epoch)
        plot_loss.append(np.mean(epoch_costs))
        if np.mean(epoch_costs) < 0.65:
            break
    print ("Unsupervised pre-training finished...")
    
    #print('encoder_3:', session.run(e_weights_h3, feed_dict={X: batch_x}))
    #print('decoder_1:', session.run(d_weights_h1, feed_dict={X: batch_x}))
    for i in range(batch_x[0].shape[0]):
        print('[batch_x reconstruction]:', batch_x[0][i], session.run(decoded[0][i], feed_dict={X: batch_x}))

    plt.plot(plot_epoch, plot_loss, 'k-')
    plt.title('AutoEncoder Loss per Generation')
    plt.xlabel('Generation')
    plt.ylabel('AutoEncoder Loss')
    plt.grid()
    plt.show()

    
    
    # ---------------- 2. Training NN - Supervised Learning ------------------ #
    for epoch in range(training_epochs):
        epoch_costs = np.empty(0)
        for b in range(total_batches):
            offset = (b * batch_size) % (train_x.shape[0] - batch_size)
            batch_x = train_x[offset:(offset + batch_size), :]
            batch_y = train_y[offset:(offset + batch_size), :]
            _, c = session.run([s_optimizer, s_cost_function],feed_dict={X: batch_x, Y : batch_y})
            epoch_costs = np.append(epoch_costs,c)
        print ("Epoch: ",epoch," Loss: ",np.mean(epoch_costs)," Training Accuracy: ", \
            session.run(accuracy, feed_dict={X: train_x, Y: train_y}), \
            "Validation Accuracy:", session.run(accuracy, feed_dict={X: val_x, Y: val_y}))
            
    print ("Supervised training finished...")
    

    print ("\nTesting Accuracy:", session.run(accuracy, feed_dict={X: test_features, Y: test_labels}))
