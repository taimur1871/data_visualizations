import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

import data_exploration

df_map = data_exploration.df_on_btm[['Bit Type', 'Bit Serial Number', 'Latitude', 'Longitude']]

fig = go.Figure(data=go.Scattergeo(
    lat=df_map.Latitude,
    lon=df_map.Longitude,
    text=df_map['Bit Serial Number'],
    mode='markers'))

fig.update_layout(
    title='Top 100 Wells',
    geo_scope='usa',
    geo_projection={'scale':5},
    geo_center={'lat':35.4676, 'lon':-97.5164}
)

fig.show()