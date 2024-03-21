#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import csv
import pickle
import json
from pandas.api.types import is_numeric_dtype
import re


# In[31]:


for delim in (',', '|', ';'):
    for decim in (',', '.'):
        df = pd.read_csv("proj2_data.csv", sep=delim, decimal=decim)
        # print(df)
        if len(df.columns) > 1 and len(df.select_dtypes(include='float').columns) > 0:
            break
    else:
        continue
    break
df.to_pickle("proj2_ex01.pkl")
df


# In[32]:


scale = {}
file1 = open("proj2_scale.txt", "r")
i = 1
for row in file1:
    scale[row.strip()] = i
    i +=1
print(scale)


# In[33]:


df1 = df.copy()
for column in df1:
    if len(df1[~df1[column].isin(scale.keys())]) == 0:
        df1[column].replace(scale, inplace=True)
df1.to_pickle('proj2_ex02.pkl')
df1


# In[39]:


df2 = df.copy()
for column in df2:
    if len(df2[~df2[column].isin(scale.keys())]) == 0:
        df2[column] = pd.Categorical(df2[column], categories=scale.keys())
df2.to_pickle('proj2_ex03.pkl')
df2.dtypes


# In[40]:


df3 = pd.DataFrame()
for col in df:
    # print(df[col].apply(lambda val: val.isnumeric()).all())
    if df.dtypes[col]!='float' and df[col].apply(lambda val: any(ch.isdigit() for ch in val)).any():
        df3[col] = df[col]
        # for var in df3[col]:
        for i in range(df.shape[0]):
            var = df3[col][i]
            print(var)
            match = re.search("-?\d+(\.\d+|\,\d+)?", var)
            if match:
                if re.search("\,|\.", match.group(0)):
                    var = float(match.group(0).replace(',','.'))
                    # print(var)
                else:
                    var = int(match.group(0))
                    # print(var)
            else:
                var = match
            df3.loc[i, col] = var
print(df3)
df3.to_pickle("proj2_ex04.pkl")


# In[41]:


i = 1
for col in df:
    list = []
    if df[col].apply(lambda val: re.search("[a-z]*", val).group(0) and val not in scale.keys()).all():
        for val in df[col]:
            if val not in list:
                list.append(val)
    if len(list) > 10:
        break
    if list:
        print(list)
        one_hot_encoded_data = pd.get_dummies(df[col]) 
        print(one_hot_encoded_data)
        one_hot_encoded_data.to_pickle(f'proj2_ex05_{i}.pkl')
        i += 1


# In[ ]:




