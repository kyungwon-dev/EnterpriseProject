
# coding: utf-8

# In[1]:


import json
import math
import numpy as np
import os

import matplotlib.pyplot as plt
import matplotlib

from matplotlib import font_manager, rc

import pandas as pd


# In[2]:


def correlation(x, y):
    n = len(x)
    vals = range(n)
 
    x_sum = 0.0
    y_sum = 0.0
    x_sum_pow = 0.0
    y_sum_pow = 0.0
    mul_xy_sum = 0.0
    
    for i in vals:
        mul_xy_sum = mul_xy_sum + float(x[i]) * float(y[i])
        x_sum = x_sum + float(x[i])
        y_sum = y_sum + float(y[i])
        x_sum_pow = x_sum_pow + pow(float(x[i]), 2)
        y_sum_pow = y_sum_pow + pow(float(y[i]), 2)
    
    try:
        r = ((n * mul_xy_sum) - (x_sum * y_sum)) / math.sqrt( ((n*x_sum_pow) - pow(x_sum, 2)) * ((n*y_sum_pow) - pow(y_sum, 2)) )
    except:
        r = 0.0
    
    return r


# In[6]:


font_location = "c:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)

filepath = os.listdir("C:/python/env_deeplearning/Enterprise/project/data")
#print(filepath)
month_per_crime = pd.read_csv('./data/%s' % filepath[0], engine='python',encoding='cp949',index_col=0,error_bad_lines=False)
location_per_crime = pd.read_csv('./data/%s' % filepath[1], engine='python',encoding='cp949',index_col=0,error_bad_lines=False)

pd.read_csv('./data/%s' % filepath[1], engine='python',encoding='cp949',index_col=0,error_bad_lines=False)

stn = ["서울","경남","경북","제주","전남","강원","충남","충북","부산","대구","인천","광주","대전","울산","경기","전북"]

pd.read_csv('./data/%s' % filepath[1], engine='python',encoding='cp949',index_col=0,error_bad_lines=False)


# In[22]:


def ScatterGraph(table,filepath,ind,a,b):
    
    fig = plt.figure()
    for i in range(0,5):
        fig.suptitle(filepath[ind] + ' 상관관계 분석')
        
        plt.subplot(1, 9, 1)
        plt.xlabel(a[i])
        plt.ylabel(b[0])
        r1 = correlation(list(table[a[i]]), list(table[b[0]]))
        plt.title('r = {:.5f}'.format(r1))
        plt.scatter(list(table[a[i]]), list(table[b[0]]), edgecolor='none', alpha=0.75, s=6, c='black')

        plt.subplot(1, 9, 3)
        plt.xlabel(a[i])
        plt.ylabel(b[1])
        r1 = correlation(list(table[a[i]]), list(table[b[1]]))
        plt.title('r = {:.5f}'.format(r1))
        plt.scatter(list(table[a[i]]), list(table[b[1]]), edgecolor='none', alpha=0.75, s=6, c='black')

        plt.subplot(1, 9, 5)
        plt.xlabel(a[i])
        plt.ylabel(b[2])
        r1 = correlation(list(table[a[i]]), list(table[b[2]]))
        plt.title('r = {:.5f}'.format(r1))
        plt.scatter(list(table[a[i]]), list(table[b[2]]), edgecolor='none', alpha=0.75, s=6, c='black')

        plt.subplot(1, 9, 7)
        plt.xlabel(a[i])
        plt.ylabel(b[3])
        r1 = correlation(list(table[a[i]]), list(table[b[3]]))
        plt.title('r = {:.5f}'.format(r1))
        plt.scatter(list(table[a[i]]), list(table[b[3]]), edgecolor='none', alpha=0.75, s=6, c='black')

        plt.subplot(1, 9, 9)
        plt.xlabel(a[i])
        plt.ylabel(b[4])
        r1 = correlation(list(table[a[i]]), list(table[b[4]]))
        plt.title('r = {:.5f}'.format(r1))
        plt.scatter(list(table[a[i]]), list(table[b[4]]), edgecolor='none', alpha=0.75, s=6, c='black')
        
        plt.show()
    return 


# In[23]:


for ind in range(2,18):
    crime = pd.read_csv('./data/%s' % filepath[ind], engine='python',encoding='cp949',index_col=0,error_bad_lines=False)
    crime = crime.tail(36)
    
    crime = crime.reset_index(drop = True)

    location_rate = location_per_crime[location_per_crime['위치']==stn[ind-2]]
    location_rate = location_rate.drop('위치', 1)
    location_rate = location_rate.values.tolist()

    location_res = month_per_crime.drop("날짜",1)
    location_res = location_res.values.tolist()

    result = []                 
    a = []

    for i in range(0,len(location_rate)):
        for j in range(0,12):
            for k in range(0,5):
                a.append("{0:.2f}".format(location_res[j+(i*12)][k]* location_rate[i][k]*0.01))
            result.append(a)
            a = []

    df = pd.DataFrame(result, columns=['강도','살인', '강간', '절도', '폭행'])
    table = pd.merge(crime, df , left_index=True, right_index=True)
    
    
    
    a = ['강도','살인', '강간', '절도', '폭행']
    b = ['평균기온','평균운량','상대습도','평균평속','일강수량']

    ScatterGraph(table,filepath,ind,a,b)
    


# In[24]:


table

