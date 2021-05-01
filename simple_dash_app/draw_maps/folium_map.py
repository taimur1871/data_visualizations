# python3

import folium
import pandas as pd

import data_exploration

# get map dataframe
df_map = data_exploration.df_on_btm[['Bit Type', 'Bit Serial Number',
                                     'Latitude', 'Longitude']]
df_map = df_map.dropna()

# create folium map
map_clusters = folium.Map(location=[35.4676, -97.5164], zoom_start=8)

# create colormap
#rainbow = [colors.rgb2hex(i) for i in range(2)]

# add markers to the map
markers_colors = []
for lat, lon, btype in zip(df_map['Latitude'], df_map['Longitude'], df_map['Bit Type']):
    label = folium.Popup('Bit Type: ' + btype, parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color='red',
        fill=True,
        #fill_color=rainbow[int(cluster)-1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters.save('./saved_html/test_map.html')
