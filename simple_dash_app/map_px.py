import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

import data_exploration
import random_coord

#df_map = data_exploration.df_on_btm[['Bit Type', 'Bit Serial Number', 'Latitude', 'Longitude', 'Distance']]
df_map = random_coord.df

# make map
#fig = px.scatter_mapbox(df_map, lat='Latitude', lon='Longitude', hover_name='Bit Type', hover_data=['Bit Serial Number'],
#                        size='Distance', color_discrete_sequence=['red'], zoom=12)
fig = px.scatter_mapbox(df_map, lat='Latitude', lon='Longitude', size='Distance', color_discrete_sequence=['red'], zoom=8)

# show street map
fig.update_layout(mapbox_style="open-street-map")

# show geographical version
fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

with open('example_map.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn'))