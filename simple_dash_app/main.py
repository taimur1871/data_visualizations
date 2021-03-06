import dash
import dash_core_components as dcc
from dash_core_components.RadioItems import RadioItems
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.Div import Div
import plotly.express as px

import pandas as pd
import numpy as np

df = pd.read_csv('./data/Mid-Con ToolRun.csv')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config["suppress_callback_exceptions"] = True

app.layout = html.Div(
    [
        html.Center(
            html.H3('Bit Offset Analysis')
            ),
        html.Div(
            children=[                
                dcc.RadioItems(
                    id='application',
                    options=[{'label':i, 'value':i} for i in df['Dir Type'].unique()],
                    value = 'V',
                    labelStyle={'display':'inline-block'}
                ),
                dcc.Dropdown(
                    id='bit-size-dropdown',
                    options = [{'label':i, 'value':i} for i in df['Bit Size'].unique()],
                    value=12.25,
                ),
                dcc.Graph(id='map-w-radio'),
            ],
            className="pretty_container six columns",
            id="map"
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id='year-slider',
                    options = [{'label':i, 'value':i} for i in df['Bit Size'].unique()],
                    value=12.25,
                ),
                dcc.Graph(id='graph-with-slider'),
            ],
            className="pretty_container five columns",
            id="basic"
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id='fm',
                    options = [{'label':i, 'value':i} for i in df['Formation Summary'].unique()],
                    value='MRMC',
                ),
                dcc.Graph(id='scatter-w-radio'),
            ],
            className="pretty_container six columns",
            id="scatter"
        ),
        html.Div(
            [
                dcc.Slider(
                    id='distance',
                    min=df['Distance'].min(),
                    max=df['Distance'].max(),
                    value=df['Distance'].min(),
                    step=None,
                ),
                dcc.Graph(id='scatter-perf'),
            ],
            className="pretty_container five columns",
            id="scatter-int"
        ),
    ]
)

# call backs
# function for map
@app.callback(
    Output('map-w-radio', 'figure'),
    Input('application', 'value'),
    Input('bit-size-dropdown','value'))
def update_figure(application, bit_size):
    filtered_df = df[(df['Dir Type'] == application) & (df['Bit Size']==bit_size)]

    fig = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude', 
                            hover_data=['Official Well Name'], 
                            color_discrete_sequence=["black"],zoom=8)

    fig.update_layout(mapbox_style="open-street-map",
                    clickmode='event+select',
                    transition_duration=0
                    )
    #fig.update_layout(clickmode='event+select')
    #fig.update_layout(transition_duration=0)

    return fig

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('map-w-radio', 'selectedData'))
def update_figure(bit_size, coord):
    filtered_df = df[(df['Bit Size'] == bit_size)]
    df_coord = pd.DataFrame(coord['points'])
    df_val = df_coord[['lon','lat']].drop_duplicates()
    
    #convert coord to np
    coord_np = df_val.to_numpy()
    filtered_df = filtered_df[filtered_df.Longitude.isin(coord_np[:,0])]

    fig = px.scatter(filtered_df, x="Distance", y="ROP", color="Bit Mfg")

    fig.update_layout(transition_duration=0)

    return fig

@app.callback(
    Output('scatter-w-radio', 'figure'),
    Input('fm','value'))
def update_figure(fm):
    filtered_df = df[df['Formation Summary']==fm]

    fig = px.scatter(filtered_df, x="Distance", y="ROP", color="Bit Mfg")

    fig.update_layout(transition_duration=0)

    return fig

@app.callback(
    Output('scatter-perf', 'figure'),
    Input('distance', 'value'),
    )
def update_figure(dist):
    filtered_df = df[df['Distance'] > int(dist)]

    fig = px.scatter(filtered_df, x="Distance", y="ROP", color="Bit Mfg")

    fig.update_layout(transition_duration=0)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)