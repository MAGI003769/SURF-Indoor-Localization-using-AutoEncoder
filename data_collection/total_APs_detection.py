import numpy as np
import pandas as pd

dataset = pd.read_csv("userinput.csv", header=0)
total_APs = list(dataset.ix[:,4])
total_APs = list(set(total_APs))

print(len(total_APs))

dic ={}

for i in range(len(total_APs)):
    dic[total_APs[i]] = i


print('BSSID', '\t', 'NO.')
for key in sorted(dic.keys()):
    print (key, '\t', dic[key])

mapping = pd.DataFrame.from_dict(dic, 'index')
mapping.to_csv('mapping.csv', header=0)
