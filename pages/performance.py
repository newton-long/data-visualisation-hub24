import base64
import sqlite3
from io import StringIO

import dash
from dash import Dash, dcc, html, Output, Input, callback, State
import dash_bootstrap_components as dbc
from Helper_Functions import *

dash.register_page(__name__)

layout = dbc.Container(
    [
        # Leading row
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Page 1 Content", className='text-center'),
                ),
            ]
        ),
        # Row that contains description of Page 1
        dbc.Row(
            dbc.Col(
                dcc.Markdown("This is the content for Page 1."),
            ),
            className='mb-4',
        ),
        # ... add more content specific to Page 1 ...
    ],
    fluid=True,
)
