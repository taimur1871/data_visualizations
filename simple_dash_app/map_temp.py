import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px

import data_exploration

# get data for the charts
df_map = data_exploration.df_on_btm[['Bit Type', 'Bit Serial Number', 'Latitude', 'Longitude', 'Distance']]
df = pd.read_csv('A2658')

# draw charts
fig = go.Figure(go.Scattermapbox(lat=df_map.Latitude, lon=df_map.Longitude))

#fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=-97)
fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=-97)
fig.update_layout(margin={"r":100,"t":100,"l":100,"b":100})

fig.show()