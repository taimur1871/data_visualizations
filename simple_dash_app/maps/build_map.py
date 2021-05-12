# python3
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

def generate_well_map(dff, selected_data, style):
    """
    Generate well map based on selected data.

    :param dff: dataframe for generate plot.
    :param selected_data: Processed dictionary for plot generation with defined selected points.
    :param style: mapbox visual style.
    :return: Plotly figure object.
    """

    layout = go.Layout(
        clickmode="event+select",
        dragmode="lasso",
        showlegend=True,
        autosize=True,
        hovermode="closest",
        margin=dict(l=0, r=0, t=0, b=0),
        mapbox=go.layout.Mapbox(
            bearing=0,
            center=go.layout.mapbox.Center(lat=37.497562, lon=-82.755728),
            pitch=0,
            zoom=8,
            style=style,
        ),
        legend=dict(
            bgcolor="#1f2c56",
            orientation="h",
            font=dict(color="white"),
            x=0,
            y=0,
            yanchor="bottom",
        ),
    )

    formations = dff["fm_name"].unique().tolist()

    data = []

    for formation in formations:
        selected_index = None
        if formation in selected_data:
            selected_index = selected_data[formation]

        text_list = list(
            map(
                lambda item: "Well ID:" + str(int(item)),
                dff[dff["fm_name"] == formation]["RecordNumber"],
            )
        )
        op_list = dff[dff["fm_name"] == formation]["op"].tolist()

        text_list = [op_list[i] + "<br>" + text_list[i] for i in range(len(text_list))]

        new_trace = go.Scattermapbox(
            lat=dff[dff["fm_name"] == formation]["nlat83"],
            lon=dff[dff["fm_name"] == formation]["wlon83"],
            mode="markers",
            marker={"color": "black", "size": 8},
            text=text_list,
            name=formation,
            selectedpoints=selected_index,
            customdata=dff[dff["fm_name"] == formation]["RecordNumber"],
        )
        data.append(new_trace)

    return {"data": data, "layout": layout}