import numpy as np
import pandas as pd

dataset = pd.read_csv('oneTime.csv', header = 0)

RSS = np.asarray(dataset.ix[:, 1])

labels = []
devices = []
time = []
for i in range(len(RSS)):
	if i % 200 == 0:
		labels.append(dataset.ix[i,2])
		devices.append(dataset.ix[i,3])
		time.append(dataset.ix[i,4])

RSS = RSS.reshape([int(RSS.shape[0]/200), 200])
labels = np.asarray(labels).reshape([len(labels), 1])
devices = np.asarray(devices).reshape([len(devices), 1])
time = np.asarray(time).reshape([len(time), 1])

dataset = np.hstack((RSS, labels, devices, time))
print(dataset.shape)
print(dataset[:, -1])

new = pd.DataFrame(dataset)
new.to_csv('test_set.csv', header = 0)