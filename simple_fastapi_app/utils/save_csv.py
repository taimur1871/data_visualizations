import os
import pandas as pd

#folder = input('Enter Folder Path\n')
stat_folder = './stat_store'

def save_csv(dataframe, serial_num):
    dataframe.to_csv(os.path.join(stat_folder, serial_num))
