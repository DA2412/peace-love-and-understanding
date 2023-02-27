# -*- coding: utf-8 -*-
"""
Created on Thu May 26 14:21:59 2022

@author: abate
"""

import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import pandas as pd
import numpy as np
sns.set_style("darkgrid")
sns.set(font_scale = 1.8)

############ LOADING DATABASE GREAT POWER WARS
inFile = "GreatPowerWarsCSV.csv"
df = pd.read_csv(inFile,index_col=0,sep=";")
df.describe()

df["duration"] = df["END"] - df["START"]

time = np.arange(df["START"].min(),df["END"].max()+1,1)
warFlag = np.zeros(len(time))
warFlag_number= np.zeros(len(time))

for j in range(0,len(df)):
    ind_War = np.where(np.logical_and(np.greater_equal(time,df['START'][j]),
                         np.less_equal(time,df['END'][j])))
    warFlag_number[ind_War]=warFlag_number[ind_War]+1
    warFlag[ind_War]=1
    
dict_war = {'time': time, 'Years_War': warFlag, 'number_wars': warFlag_number}
df = pd.DataFrame(data=dict_war)

fig,ax = plt.subplots(1,2,figsize=(20,4))
#plt.figure(figsize=(10,10))
sns.lineplot(x="time", y="number_wars",data=df,ax=ax[0])
ax[0].set_ylabel("Number of contemporary wars")

x_min = int(df["time"].min())#minimum value
x_max = int(df["time"].max())#Maximum value
numYears = 100
range_bin_num = int(np.floor((x_max-x_min)/numYears))#num binf corresponding to numYears years
width_bin = (df.time.max()-df.time.min())/4

x = df.time
y = df.Years_War
sns.histplot(df, x="time",hue="Years_War",multiple="stack",bins=range_bin_num,ax=ax[1])
#ax=sns.displot(df, x="time",hue="Years_War",multiple="stack",bins=range_bin_num,
#              kind="hist",  linewidth=2,legend=False,height=6,aspect=1.2)
ax[1].set_ylabel("Years")
ax[1].set_ylim([0, width_bin])
ax[1].set_yticks(np.append(np.arange(0, width_bin, 25),width_bin))
plt.legend(title='Years in', loc='upper center', 
    bbox_to_anchor=(.8, 1.),
    ncol=1, 
    labels=['war', 'peace'])


## PROXY WARS
inFile = "proxyWarsCSV.csv"
df_proxy = pd.read_csv(inFile,index_col=0,sep=";")
df_proxy.describe()

df_proxy['END'].replace('present', 2022,inplace=True)
df_proxy['END']=df_proxy['END'].astype(np.int64)

df_proxy["duration"] = df_proxy["END"] - df_proxy["START"]

time_proxy = np.arange(df_proxy["START"].min(),df_proxy["END"].max()+1,1)
warFlag_proxy = np.zeros(len(time_proxy))
warFlag_number_proxy= np.zeros(len(time_proxy))

for j in range(0,len(df_proxy)):
    ind_War = np.where(np.logical_and(np.greater_equal(time_proxy,df_proxy['START'][j]),
                         np.less_equal(time_proxy,df_proxy['END'][j])))
    warFlag_number_proxy[ind_War]=warFlag_number_proxy[ind_War]+1
    warFlag_proxy[ind_War]=1

## new database   
dict_war_proxy = {'time': time_proxy, 'War_condition': warFlag_proxy,
                  'number_wars': warFlag_number_proxy}
df_proxy_2 = pd.DataFrame(data=dict_war_proxy)

fig,ax = plt.subplots(1,2,figsize=(15,4))
sns.lineplot(x="time", y="number_wars",data=df_proxy_2,ax=ax[0])
ax[0].set_ylabel("Number of contemporary proxy wars")

x_min = int(df_proxy_2["time"].min())#minimum value
x_max = int(df_proxy_2["time"].max())#Maximum value
numYears = 25
range_bin_num = int(np.floor((x_max-x_min)/numYears))#num binf corresponding to numYears years
sns.histplot(df_proxy_2, x="time",hue="War_condition",multiple="stack",bins=range_bin_num,ax=ax[1])
#sns.displot(df_proxy_2, x="time",hue="Years_War",multiple="stack",bins=range_bin_num,
#              kind="hist",  linewidth=2,legend=False,height=6,aspect=1.2)
ax[1].legend(title='Years with', loc='upper center', bbox_to_anchor=(.8, 1.), ncol=1, labels=['proxy wars'])
ax[1].set_ylabel("Years")
