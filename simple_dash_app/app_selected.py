import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df = pd.read_csv('/home/taimur/Documents/DarkCirrus Projects/Analyzing Bit Records/data_visualizations/simple_dash_app/data/Mid-Con ToolRun.csv')

fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', hover_data=['Official Well Name'],
                    color_discrete_sequence=["red"],zoom=10)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(clickmode='event+select')

fig.update_traces(marker_size=6)

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    html.Div(className='row', children=[
        
        html.Div([
            dcc.Markdown("""
                **Selection Data**
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='five columns'),

        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='five columns')
    ])
])

# call backs
@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    coord_list = []
    for i in selectedData['points']:
        coord_list.append((i['lat'], i['lon']))
    return coord_list[0]


@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True, port=8010)