import dash_core_components as dcc
import dash_html_components as html


from utils import Header, make_dash_table

import pandas as pd
import pathlib

# Multi-dropdown options
from control_process import controls
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

# Create controls
county_options, well_status_options, well_type_options = controls()

# Create app layout
def create_layout(app):
    return html.Div(
        [
            dcc.Store(id="aggregate_data"),
            # empty Div to trigger javascript file for graph resizing
            html.Div(id="output-clientside"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("dash-logo.png"),
                                id="plotly-image",
                                style={
                                    "height": "60px",
                                    "width": "auto",
                                    "margin-bottom": "25px",
                                },
                            )
                        ],
                        className="one-third column",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "New York Oil and Gas",
                                        style={"margin-bottom": "0px"},
                                    ),
                                    html.H5(
                                        "Production Overview", style={"margin-top": "0px"}
                                    ),
                                ]
                            )
                        ],
                        className="one-half column",
                        id="title",
                    ),
                    html.Div(
                        [
                            html.A(
                                html.Button("Learn More", id="learn-more-button"),
                                href="https://plot.ly/dash/pricing/",
                            )
                        ],
                        className="one-third column",
                        id="button",
                    ),
                ],
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P(
                                "Filter by construction date (or select range in histogram):",
                                className="control_label",
                            ),
                            dcc.RangeSlider(
                                id="year_slider",
                                min=1960,
                                max=2017,
                                value=[1990, 2010],
                                className="dcc_control",
                            ),
                            html.P("Filter by well status:", className="control_label"),
                            dcc.RadioItems(
                                id="well_status_selector",
                                options=[
                                    {"label": "All ", "value": "all"},
                                    {"label": "Active only ", "value": "active"},
                                    {"label": "Customize ", "value": "custom"},
                                ],
                                value="active",
                                labelStyle={"display": "inline-block"},
                                className="dcc_control",
                            ),
                            dcc.Checklist(
                                id="lock_selector",
                                options=[{"label": "Lock camera", "value": "locked"}],
                                className="dcc_control",
                                value=[],
                            ),
                            html.P("Filter by well type:", className="control_label"),
                            dcc.RadioItems(
                                id="well_type_selector",
                                options=[
                                    {"label": "All ", "value": "all"},
                                    {"label": "Productive only ", "value": "productive"},
                                    {"label": "Customize ", "value": "custom"},
                                ],
                                value="productive",
                                labelStyle={"display": "inline-block"},
                                className="dcc_control",
                            ),
                            dcc.Dropdown(
                                id="well_names",
                                options=None,
                                multi=True,
                                value=list(None),
                                className="dcc_control",
                            ),
                        ],
                        className="pretty_container four columns",
                        id="cross-filter-options",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [html.H6(id="well_text"), html.P("No. of Wells")],
                                        id="wells",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(id="gasText"), html.P("Gas")],
                                        id="gas",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(id="oilText"), html.P("Oil")],
                                        id="oil",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(id="waterText"), html.P("Water")],
                                        id="water",
                                        className="mini_container",
                                    ),
                                ],
                                id="info-container",
                                className="row container-display",
                            ),
                            html.Div(
                                [dcc.Graph(id="count_graph")],
                                id="countGraphContainer",
                                className="pretty_container",
                            ),
                        ],
                        id="right-column",
                        className="eight columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(id="main_graph")],
                        className="pretty_container seven columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="individual_graph")],
                        className="pretty_container five columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(id="pie_graph")],
                        className="pretty_container seven columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="aggregate_graph")],
                        className="pretty_container five columns",
                    ),
                ],
                className="row flex-display",
            ),
        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
    )