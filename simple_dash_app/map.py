import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

import data_exploration

# get data for the charts
df_map = data_exploration.df_on_btm[['Bit Type', 'Bit Serial Number', 'Latitude', 'Longitude']]
df = pd.read_csv('A2658')

# draw charts
fig = make_subplots(rows = 2, cols = 2,
                    specs=[[{"type": "xy"}, {"type": "domain"}],
                           [{"type": "scattermapbox"}, {"type": "domain"}]],
                    )

fig.add_trace(go.Scatter(x = df['adj_x'], y = df['adj_y'],
                         mode='markers'), row=1, col=1)

fig.add_trace(go.Scattermapbox(lat=df_map.Latitude, lon=df_map.Longitude,
                            text=df_map['Bit Serial Number'],
                            mode='markers'), row=2, col=1)

fig.add_trace(go.Pie(labels = df.wear.value_counts().index,
                     values = df['wear'].value_counts().values),
              row=1, col=2)

fig.add_trace(go.Pie(labels = df['wear_type'].value_counts().index,
                     values = df['wear_type'].value_counts().values),
                row=2, col=2)

fig.update_geos(
    landcolor='lightgreen',
    oceancolor='MidnightBlue',
    showocean=True,
    lakecolor='LightBlue',
    scope='usa',
    projection_scale=5,
    center={'lat':35.4676, 'lon':-97.5164},
    subunitcolor='black',
    domain_row=2,
    domain_column=1,
    )

fig.show()