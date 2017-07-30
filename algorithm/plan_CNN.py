import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
from sklearn.preprocessing import scale

dataset = pd.read_csv(".\\UJIndoorLoc\\trainingData.csv",header = 0)
features = scale(np.asarray(dataset.ix[:,0:520]))

# --------------------- Training and validation set --------------- #

# Convert RSS vector into 26*20 matrix
maps = []
for i in range (features.shape[0]):
    temp_map = np.reshape(features[i,:], (26, 20, 1))
    maps.append(temp_map)
maps = np.asarray(maps)
labels = np.asarray(dataset["BUILDINGID"].map(str) + dataset["FLOOR"].map(str))
labels = np.asarray(pd.get_dummies(labels))

print('labels shape:', labels.shape)
print(maps.shape)

train_val_split = np.random.rand(len(features)) < 0.90
train_x = maps[train_val_split]
train_y = labels[train_val_split]
val_x = maps[~train_val_split]
val_y = labels[~train_val_split]

# --------------------- Testing set --------------- #

test_dataset = pd.read_csv(".\\UJIndoorLoc\\validationData.csv",header = 0)
test_features = scale(np.asarray(test_dataset.ix[:,0:520]))
# Convert RSS vector into 26*20 matrix
test_maps = []
for i in range (test_features.shape[1]):
    temp_map = np.reshape(test_features[i,:], (26, 20, 1))
    test_maps.append(temp_map)
test_labels = np.asarray(test_dataset["BUILDINGID"].map(str) + test_dataset["FLOOR"].map(str))
test_labels = np.asarray(pd.get_dummies(test_labels))

# --------------------- Def functions for variable declaration --------------- #

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.1, dtype=tf.float32)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0, shape = shape, dtype=tf.float32)
    return tf.Variable(initial)

# --------------------- Model parameters --------------- #

learning_rate = 0.01
training_epochs = 20
batch_size = 500
map_width = train_x[0].shape[0]
map_height = train_x[0].shape[1]
num_channels = 1

n_input = 520 
n_hidden_1 = 256 
n_hidden_2 = 128 
n_hidden_3 = 64 

n_classes = labels.shape[1]

conv_kernel = 4
conv1_features = 25
conv2_features = 50
max_pool_size1 = 2 # NxN window for 1st max pool layer
max_pool_size2 = 2 # NxN window for 2nd max pool layer
fully_connected_size1 = 100
keep_prob = 1

total_batches = dataset.shape[0] // batch_size

# --------------------- Placeholders --------------- #

x_input_shape = (None, map_width, map_height, num_channels)
X = tf.placeholder(tf.float32, shape=x_input_shape)
Y = tf.placeholder(tf.int32, shape = (None, n_classes))

# --------------------- Initailize model --------------- #
def my_conv_net(input_data):
    # 1st layer: 100C3-MP2
    conv_1 = slim.conv2d(input_data, 100, [3, 3], 1, padding='SAME', scope='conv1',activation_fn=tf.nn.relu)
    max_pool1 = slim.max_pool2d(conv_1, [2, 2], [2, 2], padding='SAME')

    # 2nd layer: 200C2-MP2
    conv_2 = slim.conv2d(max_pool1, 200, [2, 2], 1, padding='SAME', scope='conv2',activation_fn=tf.nn.relu)
    max_pool2 = max_pool_1 = slim.max_pool2d(conv_2, [2, 2], [2, 2], padding='SAME')

    # Flat the output from conv layers for next fully connected layers
    flatten = slim.flatten(max_pool2)
    
    # 1st fully connected layer
    fc1 = slim.fully_connected(slim.dropout(flatten, keep_prob), 1024,
                                   activation_fn=tf.nn.tanh, scope='fc1')

    # 2nd fully connected layer
    model_output = slim.fully_connected(slim.dropout(fc1, keep_prob), n_classes,
                                   activation_fn=None, scope='fc2')

    return(model_output)


model_output = my_conv_net(X)

# Declare Loss Function (softmax cross entropy)
loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=model_output, labels=tf.reduce_max(Y,1)))

# Create a prediction function
prediction = tf.nn.softmax(model_output)

# Create an optimizer
my_optimizer = tf.train.AdamOptimizer(learning_rate)
train_step = my_optimizer.minimize(loss)

# Calculate accuracy function
# In this function, batch_prediction is the ouput result from the CNN
# while labels are the real label stored in dataset which trains the model
def get_acc(logists, labels):
    batch_predictions = np.argmax(logists, axis=1)
    bingo = np.sum(np.equal(batch_predictions, labels))
    return(100. * bingo/batch_predictions.shape[0])

train_loss = []
train_acc = []
test_acc = []

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    for epoch in range(training_epochs):
        epoch_loss = np.empty(0)
        epoch_acc = np.empty(0)
        for b in range(total_batches):
            offset = (b * batch_size) % (train_x.shape[0] - batch_size)
            batch_x = train_x[offset:(offset + batch_size), :]
            batch_y = train_y[offset:(offset + batch_size), :]

            sess.run(train_step, feed_dict={X: batch_x, Y : batch_y})
            batch_prediction, batch_loss = sess.run([prediction, loss], feed_dict={X: batch_x, Y : batch_y})
            batch_acc = get_acc(batch_prediction, batch_y)
            print("batch_pre:", batch_prediction.shape)
            epoch_loss = np.append(epoch_loss, batch_loss)
            print("!!!!!")
            epoch_acc = np.append(epoch_acc, batch_acc)
            print(b)
        print ("Epoch: ",epoch," Loss: ",np.mean(epoch_loss)," Training Accuracy: ", \
            sess.run(np.mean(epoch_acc), feed_dict={X: train_x, Y: train_y}), \
            "Validation Accuracy:", sess.run(accuracy, feed_dict={X: val_x, Y: val_y}))
    print ("Supervised training finished...")