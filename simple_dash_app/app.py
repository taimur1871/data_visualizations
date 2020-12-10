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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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

fig.add_trace(go.Pie(labels = df_bits.index.values,
                     values = df_bits['count']),
              row=1, col=2)

fig.add_trace(go.Pie(labels = df_bits.index.values,
                     values = df_bits['count']),
              row=2, col=2)

app.layout = html.Div(style={'backgroundColor': colors['background']},
    children=[
    html.H1(children='Bit Offset Analysis',
            style={
            'color': colors['text']
        }),

    html.H4(children='''
        Baby steps towards the dashboard
    ''',
             style={
            'color': colors['text']
        }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
