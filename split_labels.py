#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
time:
"""
#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import os
np.random.seed(1)


#split csv 
totalsample_csv_path = r'C:\vue\label_transform\data/raccoon_labels.csv'
split_CSV_save_path = r'C:\vue\label_transform\data'

train_ratio = 0.8

full_labels = pd.read_csv(totalsample_csv_path)
gb = full_labels.groupby('filename')
grouped_list = [gb.get_group(x) for x in gb.groups]
total_sample_num = len(grouped_list)
train_num =  int(total_sample_num * train_ratio)

train_index = np.random.choice(total_sample_num, size= train_num, replace=False)
test_index = np.setdiff1d(list(range(total_sample_num)), train_index)

train = pd.concat([grouped_list[i] for i in train_index])
test = pd.concat([grouped_list[i] for i in test_index])

train.to_csv(os.path.join(split_CSV_save_path,'train_labels.csv'), index=None)
test.to_csv(os.path.join(split_CSV_save_path,'test_labels.csv'), index=None)




‘’‘
#split yolo_txt 
sample_txt = open('training_anguoHome.txt',"r")
lines = sample_txt.readlines()


train_ratio = 0.9

total_sample_num = len(lines)
train_num =  int(total_sample_num * train_ratio)

np.random.shuffle(lines)


list_train = lines[:train_num]
list_val = lines[train_num:]


train_txt = 'train_anguoHome.txt'
with open(train_txt, 'w') as f1:
    for item in list_train:
        f1.write(item)


vaild_txt = 'vaild_anguoHome.txt'
with open(vaild_txt, 'w') as f2:
    for item in list_train:
        f2.write(item)
        
’‘’
