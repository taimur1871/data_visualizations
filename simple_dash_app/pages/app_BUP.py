# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
#from plotly.subplots import make_subplots

from utils import data_exploration

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=external_stylesheets
    )

colors = {
    'background': '#DDD7D6',
    'text': '#000000'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_on_btm = data_exploration.df_on_btm
df_bits = data_exploration.df_bits
df_map = data_exploration.df_on_btm[['Bit Type', 'Bit Serial Number', 'Latitude', 'Longitude']]

fig = go.Figure(go.Scatter(x = df_on_btm['Distance'], y = df_on_btm['ROP'],
                         mode='markers'))

fig1 = go.Figure(go.Pie(labels = df_bits.index.values,
                     values = df_bits['count']))

fig2 = go.Figure(go.Pie(labels = df_on_btm['Bit Mfg'].values,
                     values = df_bits['count']))

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

# make map
fig3 = px.scatter_mapbox(df_map, lat='Latitude', lon='Longitude',
                        color_discrete_sequence=['red'], zoom=6)

fig3.update_layout(mapbox_style="open-street-map")
fig.update_geos(center={'lon':35.4676, 'lat':-97.5164})

app.layout = html.Div(
        id="root",
        style={'backgroundColor': colors['background']},
        children=[
                html.H1(children='Bit Offset Analysis',
                        style={
                                'color': colors['text']
                            }),
                html.H4(children='Offset Analysis Demo Page',
                        style={
                                'color': colors['text']
                            }),
                dcc.Graph(
                        id='example-graph',
                        figure=fig
                        ),
                dcc.Graph(
                        id='bit-pie-graph',
                        figure=fig1
                        ),
                dcc.Graph(
                        id='wear-pie-graph',
                        figure=fig1
                        ),
                
                html.Div(
                        id="heatmap-container",
                        children=[
                            html.P(
                                "Map Example"
                                ),
                            dcc.Graph(
                                id="well-location",
                                figure=fig3 ),
                            ]),
                                            ],)

'''@app.callback(
    Output("well-location", "figure"),
    [Input("example-graph", "Figure")],
    )'''

def display_map(df_map, fig1):

    data = [
        dict(
            lat=df_map.Latitude,
            lon=df_map.Longitude,
            text=df_map['Bit Serial Number'],
            type="scattermapbox",
            hoverinfo="text",
            marker=dict(size=5, color="black", opacity=0),
        )
    ]

    layout = dict(
        mapbox=dict(
            layers=[],
            accesstoken=mapbox_access_token,
            style=mapbox_style,
            center=dict(lat=35.4676, lon=-97.5164),
            zoom=5,
        ),
        hovermode="closest",
        margin=dict(r=0, l=0, t=0, b=0),
        annotations=df_map['Bit Serial Number'],
        dragmode="lasso",
    )

    fig = dict(data=data, layout=layout)
    return fig

'''@app.callback(Output("well-location", "children"),
            [Input("years-slider", "value")],)
def update_map_title(year):
    return "Heatmap of age adjusted mortality rates \
				from poisonings in year {0}".format(
        year
    )'''

if __name__ == '__main__':
    app.run_server(debug=True)
