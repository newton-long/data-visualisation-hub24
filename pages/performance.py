import base64
import sqlite3
from io import StringIO

import dash
from dash import Dash, dcc, html, Output, Input, callback, State
import dash_bootstrap_components as dbc
from Helper_Functions import *

dash.register_page(__name__)

"""
Contains the layout for the performance analytics of advisors. 
"""
layout = dbc.Container(
    [
        # Leading row
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Advisor Performance Tracker", className='text-center'),
                ),
            ]
        ),
        # Row that contains description of Page 1
        dbc.Row(
            dbc.Col(
                dcc.Markdown("Please upload your advisor data:"),
            ),
            className='mb-4',
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            "Drag and Drop or ",
                            html.A('Select Files', className="bold-text")
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=False
                    ),
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='advisor-upload', children='Upload status will be displayed here.')
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Button('Generate Output', id='button', n_clicks=0,
                                className='btn btn-primary',
                                style={'margin-top': '10px', 'border-radius': '8px'})
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='perf-vis', figure=default_graph())
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H3("Most Successful Account ID?")
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    # To display the best performing account thus we can track best performing advisor...
                    html.Div(id="text-output",
                             children=html.Div("")
                             )
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id="2ndoutput",
                             children=html.Div("")
                             )
                )
            ]
        )
    ],
    fluid=True,
)


@callback(
    Output('advisor-upload', 'children'),
    Input('upload-data', 'contents'),
    prevent_initial_call=True
)
def upload_status(contents):
    if contents is not None:
        # Decode the contents to get the file data
        content_type, content_string = contents.split(',')
        decoded_content = base64.b64decode(content_string)
        # Store into data base with sql lite
        df = pd.read_csv(StringIO(decoded_content.decode('utf-8')))
        # Currently just going to be one singular .db file -> assuming need to upload each time...
        db_connection = sqlite3.connect('performance_data.db')
        df.to_sql('performance_data_table', db_connection, if_exists='replace', index=False)
        db_connection.close()

        # For demonstration purposes, let's assume the upload was successful
        return 'File successfully uploaded 😊.'
    else:
        return 'No file uploaded 🙁.'


@callback(
    [Output('perf-vis', 'figure'),
     Output('text-output', 'children'),
     Output("2ndoutput", 'children')],
    Input('button', 'n_clicks'),
    prevent_initial_call=True
)
def generate_output(n_clicks):
    data = get_perf_data()
    if n_clicks > 0:
        return performance_line_graph(data), text_output(data), worst_account(data)
    # Check if pressed
    return None, "", ""
