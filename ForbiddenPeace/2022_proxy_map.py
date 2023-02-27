# -*- coding: utf-8 -*-
"""
Created on Thu May 26 13:44:36 2022

@author: abate
"""
from urllib.request import urlopen
import json
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)
with urlopen('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') as response:
    counties = json.load(response)

counties["features"][0]

import pandas as pd
import numpy as np
# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
#                    dtype={"fips": str})
# df["fips"]=0
# df.insert(2, 'region', 'AFG')
# df.head()
inFile = "proxyWarsGeoCSV.csv"
df_proxy = pd.read_csv(inFile,index_col=0,sep=";")
df_proxy.describe()

df_proxy['END'].replace('present', 2022,inplace=True)
df_proxy['END']=df_proxy['END'].astype(np.int64)

df_proxy["duration"] = df_proxy["END"] - df_proxy["START"]

df = df_proxy[['Country','duration','START']]
#adf = df.query('START>=1927')
df_years_war=df.groupby("Country")["duration"].mean().reset_index(name ='Avg_Years_war')

df_years_war=df.groupby("Country")["duration"].sum().reset_index(name ='sum')

df_num_wars=df.groupby("Country")["START"].count().reset_index(name ='Num_wars')
#df.groupby('Country')['duration'].transform('sum').unstack()

# plot
import plotly.express as px
import plotly.io as pio
#pio.renderers.default = 'svg'
pio.renderers.default = 'browser'

fig = px.choropleth_mapbox(df_years_war, geojson=counties, locations='Country', color='Avg_Years_war',
                           color_continuous_scale="Viridis",
                           range_color=(0, df_years_war.Avg_Years_war.max()),
                           mapbox_style="carto-positron",
                           zoom=1, center = {"lat": 40, "lon": -1},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

fig = px.choropleth_mapbox(df_num_wars, geojson=counties, locations='Country', color='Num_wars',
                           color_continuous_scale="Viridis",
                           range_color=(0, df_num_wars.Num_wars.max()),
                           mapbox_style="carto-positron",
                           zoom=1, center = {"lat": 40, "lon": -1},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
