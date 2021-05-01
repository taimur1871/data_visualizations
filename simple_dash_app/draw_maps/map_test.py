import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

import data_exploration

# get data for the charts
df_map = data_exploration.df_on_btm[['Bit Type', 'Bit Serial Number', 'Latitude', 'Longitude']]
df = pd.read_csv('A2658')

# draw charts

mapbox_access_token = 'pk.eyJ1IjoidGFpbXVyMTg3MSIsImEiOiJja243em5jamYwNHFvMnVueDNnNjJydHk3In0.kG54SYI19aPDe818kKSJqA'

fig = go.Figure(go.Scattermapbox(lat=df_map.Latitude, lon=df_map.Longitude,
                            text=df_map['Bit Serial Number'], 
                            marker=go.scattermapbox.Marker(size=10),
                            mode='markers'))

fig.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=45,
            lon=-73
        ),
        pitch=0,
        zoom=5
    )
)

fig.show()