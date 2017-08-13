import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt

from function_version import *

user_input = pd.read_csv("user_input.csv",header = 0)
user_input = np.asarray(user_input.ix[:, 0:520]).reshape([1, 520])
user_input = scale(user_input, axis=1)

def twice_call():
	location = run_model(user_input)
	return location

if __name__ == '__main__':
	location = twice_call()
	print(location)