# python 3
# import modules
import pandas as pd
import plotly.express as px

from utils import random_coord

# get data
df_map = random_coord.df

# make map
fig = px.scatter_mapbox(df_map, lat='Latitude', lon='Longitude',
                        size='Distance', color_discrete_sequence=['red'],
                        zoom=15)

# show street map
fig.update_layout(mapbox_style="open-street-map")
#fig.update_layout(mapbox_style="carto-positron")
#fig.update_layout(mapbox_style="carto-darkmatter")

# show geographical version
#fig.update_layout(mapbox_style="stamen-terrain")
#fig.update_layout(mapbox_style="stamen-toner")
#fig.update_layout(mapbox_style="stamen-watercolor")

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(center={'lon':39.89989, 'lat':-105.085513})
fig.show()

with open('./saved_html/example_map.html', 'w') as f:
        f.write(fig.to_html(include_plotlyjs='cdn'))
