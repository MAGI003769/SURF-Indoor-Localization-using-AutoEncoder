import numpy as np
import pandas as pd

dataset = pd.read_csv("test_info_data.csv", header=0)
total_APs = list(dataset.ix[:,5])
total_APs = list(set(total_APs))

print(len(total_APs))

dic ={}

for i in range(len(total_APs)):
    dic[total_APs[i]] = i

for key in sorted(dic.keys()):
    print (key, '\t', dic[key])
