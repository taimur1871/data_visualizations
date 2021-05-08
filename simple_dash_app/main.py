import dash
import dash_core_components as dcc
from dash_core_components.RadioItems import RadioItems
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.Div import Div
import plotly.express as px

import pandas as pd

df = pd.read_csv('./data/Mid-Con ToolRun.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
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
                dcc.Graph(id='map-w-radio'),
                dcc.RadioItems(
                    id='application',
                    options=[{'label':i, 'value':i} for i in df['Dir Type'].unique()],
                    value = 'H',
                    labelStyle={'display':'inline-block'}
                )
            ],
            className="pretty_container six columns",
            id="map"
        ),
    ]
)


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df['Bit Size'] == selected_year]

    fig = px.scatter(filtered_df, x="Distance", y="ROP", color="Bit Mfg",
                     log_x=False, size_max=55)

    fig.update_layout(transition_duration=0)

    return fig

@app.callback(
    Output('map-w-radio', 'figure'),
    Input('application', 'value'))
def update_figure(application):
    filtered_df = df[df['Dir Type'] == application]

    fig = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude',
                            color_discrete_sequence=["red"],zoom=6)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(transition_duration=0)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)