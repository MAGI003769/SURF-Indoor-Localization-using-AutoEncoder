import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import scale

dataset = pd.read_csv(".\\UJIndoorLoc\\trainingData.csv",header = 0)
features = scale(np.asarray(dataset.ix[:,0:520]))

# --------------------- Training and validation set --------------- #

# Convert RSS vector into 26*20 matrix
maps = []
for i in range (features.shape[0]):
    temp_map = np.reshape(features[i,:], (26, 20))
    maps.append(temp_map)
maps = np.asarray(maps)
labels = np.asarray(dataset["BUILDINGID"].map(str) + dataset["FLOOR"].map(str))
labels = np.asarray(pd.get_dummies(labels))

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
    temp_map = np.reshape(test_features[i,:], (26, 20))
    test_maps.append(temp_map)
test_labels = np.asarray(test_dataset["BUILDINGID"].map(str) + test_dataset["FLOOR"].map(str))
test_labels = np.asarray(pd.get_dummies(test_labels))

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.1, dtype=tf.float32)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0, shape = shape, dtype=tf.float32)
    return tf.Variable(initial)

# --------------------- Model parameters --------------- #

learning_rate = 0.01
training_epochs = 20
batch_size = 10
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

total_batches = dataset.shape[0] // batch_size

# --------------------- Placeholders --------------- #

x_input_shape = (batch_size, map_width, map_height, num_channels)
X = tf.placeholder(tf.float32, shape=x_input_shape)
Y = tf.placeholder(tf.float32, [None,n_classes])

# --------------------- Variables of Layers --------------- #
# Convolutional layers
conv1_weight = weight_variable([conv_kernel, conv_kernel, num_channels, conv1_features])
conv1_bias = bias_variable([conv1_features])
conv2_weight = weight_variable([conv_kernel, conv_kernel, conv1_features, conv2_features])
conv2_bias = bias_variable([conv2_features])

# fully-connected layers
resulting_width = map_width // (max_pool_size1 * max_pool_size2)#6+1=7
resulting_height = map_height // (max_pool_size1 * max_pool_size2) #5
full1_input_size = resulting_width * resulting_height * conv2_features

full1_weight = weight_variable([full1_input_size, fully_connected_size1])
full1_bias = bias_variable([fully_connected_size1])

full2_weight = weight_variable([fully_connected_size1, n_classes])
full2_bias = bias_variable([n_classes])

# --------------------- Initailize model --------------- #
def my_conv_net(input_data):
    # First Conv-ReLU-MaxPool Layer
    conv1 = tf.nn.conv2d(input_data, conv1_weight, strides=[1, 1, 1, 1], padding='SAME')
    relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_bias))
    max_pool1 = tf.nn.max_pool(relu1, ksize=[1, max_pool_size1, max_pool_size1, 1],
                               strides=[1, max_pool_size1, max_pool_size1, 1], padding='SAME')

    # Second Conv-ReLU-MaxPool Layer
    conv2 = tf.nn.conv2d(max_pool1, conv2_weight, strides=[1, 1, 1, 1], padding='SAME')
    relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_bias))
    max_pool2 = tf.nn.max_pool(relu2, ksize=[1, max_pool_size2, max_pool_size2, 1],
                               strides=[1, max_pool_size2, max_pool_size2, 1], padding='SAME')

    # Transform Output into a 1xN layer for next fully connected layer
    final_conv_shape = max_pool2.get_shape().as_list()
    print(final_conv_shape)
    final_shape = final_conv_shape[1] * final_conv_shape[2] * final_conv_shape[3]
    flat_output = tf.reshape(max_pool2, [final_conv_shape[0], final_shape])

    # First Fully Connected Layer
    fully_connected1 = tf.nn.relu(tf.add(tf.matmul(flat_output, full1_weight), full1_bias))

    # Second Fully Connected Layer
    final_model_output = tf.add(tf.matmul(fully_connected1, full2_weight), full2_bias)
    
    return(final_model_output)


model_output = my_conv_net(X)

# Create a prediction function
prediction = tf.nn.softmax(model_output)

with tf.Session() as sess:
    tf.global_variables_initializer()
    print(sess.run(prediction, {X: train_x}))