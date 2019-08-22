
# coding: utf-8

# In[86]:


import json
import math
import numpy as np
import os

import tensorflow as tf

import matplotlib.pyplot as plt
import matplotlib

from matplotlib import font_manager, rc
import datetime
import pandas as pd


# In[30]:


font_location = "c:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)

filepath = os.listdir("C:/python/env_deeplearning/Enterprise/project/data")
print(filepath)


# In[94]:



#1990 ~ 2017 ==> 27 년
# 324 = 28 * 12
total_weather = []
sum = 0
base_year = 1990
for k in range(2,18):
    file_1 = pd.read_csv('./data/%s' % filepath[k], engine='python',encoding='cp949',index_col=0)
    file_1 = file_1.values.tolist()
    for i in range(0,27):
        for j in range(0,12):
            try:
                sum = sum + float(file_1[j+(i*12)][3])
            except Exception as e:
                print(j+(i*12))
        total_weather.append([base_year+i,sum/12])
        sum = 0

sum = 0
sum_total = []
for i in range(0,27):
    for j in range(0,16):
        sum = total_weather[(j*27) + i][1]
    sum_total.append([base_year+i,sum/16])
    sum = 0
print(a)
a = np.array(sum_total)
a = a.transpose()
a = a.tolist()
b= []
b.append(a[1])
b.append(a[0])
print(b)


# In[84]:


plt.plot(b[1],b[0])
plt.xlabel('연도')
plt.ylabel('기후값')
plt.show()

