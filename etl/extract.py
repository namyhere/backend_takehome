import pandas as pd
import os

#read dataset:
def extract_data(directory, filename):
    data = pd.read_csv(directory + os.sep + filename, delimiter=",\t")
    return data