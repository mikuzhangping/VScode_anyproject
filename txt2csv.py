import re
import os
import numpy as np
import pandas as pd

if __name__ == "__main__":
    file_path = r"G:/ubuntu_ShareFiles"
    file_list = os.listdir(file_path)
    columns = ['2level1024', '2level64', 'bimod1024', 'bimod512', 'nottaken', 'taken']
    i=0
    for file in file_list:
        i+=1
        file_dir = file_path+"/"+file
        with open(file_dir, 'r') as f1:
            content = f1.read()
            print(content)
    df = pd.DataFrame(data=result, columns=columns)
    pass