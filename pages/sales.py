import dash
from dash import Dash, dcc, html, Output, Input, callback, State
import dash_bootstrap_components as dbc
from Helper_Functions import *

dash.register_page(__name__)

layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                html.H1("Sales Data Visualisations", className='text-center'),
            ),
        ]
    ),
)
