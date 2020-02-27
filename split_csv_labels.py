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

