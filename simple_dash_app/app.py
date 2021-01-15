# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
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

fig.add_trace(go.Pie(labels = df_bits.index.values(),
                     values = df_bits['count']),
              row=1, col=2)

fig.add_trace(go.Pie(labels = df_on_btm['Bit Mfg'].values,
                     values = df_bits['count']),
              row=2, col=2)

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

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
            id="county-choropleth",
            figure=dict(
                layout=dict(
                    mapbox=dict(
                        layers=[],
                        accesstoken=mapbox_access_token,
                        style=mapbox_style,
                        center=dict(
                            lat=38.72490, lon=-95.61446
                            ),
                        pitch=0,
                        zoom=6,
                        ),
                    autosize=True,
                    ),
                ),
            ),
        ],
    )
])


def display_map(year, figure):
    cm = dict(zip(BINS, DEFAULT_COLORSCALE))

    data = [
        dict(
            lat=df_lat_lon["Latitude "],
            lon=df_lat_lon["Longitude"],
            text=df_lat_lon["Hover"],
            type="scattermapbox",
            hoverinfo="text",
            marker=dict(size=5, color="white", opacity=0),
        )
    ]

    annotations = [
        dict(
            showarrow=False,
            align="right",
            text="<b>Age-adjusted death rate<br>per county per year</b>",
            font=dict(color="#2cfec1"),
            bgcolor="#1f2630",
            x=0.95,
            y=0.95,
        )
    ]

    for i, bin in enumerate(reversed(BINS)):
        color = cm[bin]
        annotations.append(
            dict(
                arrowcolor=color,
                text=bin,
                x=0.95,
                y=0.85 - (i / 20),
                ax=-60,
                ay=0,
                arrowwidth=5,
                arrowhead=0,
                bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
            )
        )

    if "layout" in figure:
        lat = figure["layout"]["mapbox"]["center"]["lat"]
        lon = figure["layout"]["mapbox"]["center"]["lon"]
        zoom = figure["layout"]["mapbox"]["zoom"]
    else:
        lat = 38.72490
        lon = -95.61446
        zoom = 3.5

    layout = dict(
        mapbox=dict(
            layers=[],
            accesstoken=mapbox_access_token,
            style=mapbox_style,
            center=dict(lat=lat, lon=lon),
            zoom=zoom,
        ),
        hovermode="closest",
        margin=dict(r=0, l=0, t=0, b=0),
        annotations=annotations,
        dragmode="lasso",
    )

    base_url = "https://raw.githubusercontent.com/jackparmer/mapbox-counties/master/"
    for bin in BINS:
        geo_layer = dict(
            sourcetype="geojson",
            source=base_url + str(year) + "/" + bin + ".geojson",
            type="fill",
            color=cm[bin],
            opacity=DEFAULT_OPACITY,
            # CHANGE THIS
            fill=dict(outlinecolor="#afafaf"),
        )
        layout["mapbox"]["layers"].append(geo_layer)

    fig = dict(data=data, layout=layout)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
