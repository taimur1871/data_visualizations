# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

import data_exploration

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets
    )

colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_on_btm = data_exploration.df_on_btm
df_bits = data_exploration.df_bits
df_map = data_exploration.df_on_btm[['Bit Type', 'Bit Serial Number', 'Latitude', 'Longitude']]

#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig = make_subplots(rows = 2, cols = 2,
                    specs=[[{"type": "xy"}, {"type": "domain"}],
                           [{"type": "xy"}, {"type": "domain"}]],
                    )

fig.add_trace(go.Scatter(x = df_on_btm['Distance'], y = df_on_btm['ROP'],
                         mode='markers'),
              row=1, col=1)

fig.add_trace(go.Scatter(x = df_on_btm['Distance'], y = df_on_btm['Hrs'],
                         mode='markers'),
              row=2, col=1)

fig.add_trace(go.Pie(labels = df_bits.index.values,
                     values = df_bits['count']),
              row=1, col=2)

fig.add_trace(go.Pie(labels = df_on_btm['Bit Mfg'].values,
                     values = df_bits['count']),
              row=2, col=2)

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

fig1 = go.Figure(data=go.Scattergeo(
    lat=df_map.Latitude,
    lon=df_map.Longitude,
    text=df_map['Bit Serial Number'],
    mode='markers'))

fig1.update_layout(
    title='Top 100 Wells',
    geo_scope='usa',
    geo_projection={'scale':5},
    geo_center={'lat':35.4676, 'lon':-97.5164}
)

app.layout = html.Div(
        id="root",
        style={'backgroundColor': colors['background']},
        children=[
                html.H1(children='Bit Offset Analysis',
                        style={
                                'color': colors['text']
                            }),
                html.H4(children='''Baby steps towards the dashboard''',
                        style={
                                'color': colors['text']
                            }),
                dcc.Graph(
                        id='example-graph',
                        figure=fig
                        ),
                
                html.Div(
                        id="heatmap-container",
                        children=[
                            html.P(
                                "Map Example"
                                ),
                            dcc.Graph(
                                id="well-location",
                                figure=fig1 ),
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
