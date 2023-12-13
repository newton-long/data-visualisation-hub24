"""
Interactive web application, for data visualisations.
Single web page -> can specify what visualisations the user is looking for.
Data provided is stored in SQL Lite database for transportable use.
"""
import base64
import sqlite3
from io import StringIO

import dash
import matplotlib.pyplot as plt
import numpy as np
from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Create instance of dash component with VAPOR aesthetic
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Layout -> constructed from ROWS (row by row)
app.layout = dbc.Container(
    [
        # Leading row
        dbc.Row(
            # Put a col in
            dbc.Col(
                html.H1("Data Visualisation Tool", className='text-center')
            ),
        ),
        # Row containing the radio buttons
        dbc.Row(
            [
                dbc.Col(
                    # Add a Divider to aggregate components together
                    html.Div([
                        html.P("Select output:"),
                        dcc.RadioItems(
                            id='spec-radio',
                            options=[
                                {'label': ' Income Vs Age', 'value': 'Income vs age data for bubble '
                                                                     'chart output.'},
                                {'label': ' Advisor Performance', 'value': 'Advisor performance data.'},
                                {'label': ' Geographical Representation', 'value': 'Postcode and income '
                                                                                   'data.'},
                            ],
                            value='Please select an output.',
                        ),
                    ]),
                    className='mb-4'
                ),
            ]
        ),
        # Row that outputs the selected output message
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='output-message')
                ),
            ],
            className="mb-4",
        ),
        # Row for the upload button
        dbc.Row(
            [
                dbc.Col(
                    dcc.Upload(
                        id='upload-data',
                        children=html.Button('Upload Data', style={'width': '100%',
                                                                   'display': 'inline-block'}),
                        multiple=False
                    ),
                    className='mb-4'
                ),
                dbc.Col(
                    dcc.Loading(
                        id='loading',
                        type='circle',
                        children=[html.Div(id='loading-output')],
                    )
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='visualisation')
                ),
            ]
        ),
    ],
    fluid=True,
)


# Helper functions -> returns dataframe...
def get_uploaded_data():
    db_connection = sqlite3.connect('uploaded_data.db')
    query = "SELECT * FROM uploaded_data_table"
    df = pd.read_sql(query, db_connection)
    db_connection.close()
    return df


def update_graph(selected_radio):
    data = get_uploaded_data()
    if selected_radio == 'bubble':
        graph = create_bubble_plot(df)
    elif selected_radio == 'perf':
        graph = create_performance_graph(df)
    elif selected_radio == 'geo':
        graph = create_geographical_graph(df)
    else:
        graph = create_default_scatter_plot(df)

    return graph


def create_bubble_plot(df):
    fig = {
        'data': [
            {
                'x': df['Income'],
                'y': df['Age'],
                'mode': 'markers',
                'type': 'scatter',
                'marker': {
                    'size': df['SomeNumericVariable'],  # Adjust size based on a numeric variable
                    'color': df['SomeColorVariable'],  # Use a color variable for shading
                    'colorscale': 'Viridis',  # Choose a color scale (e.g., Viridis)
                    'colorbar': {'title': 'Colorbar Title'}  # Add a colorbar with a title
                }
            }
        ],
        'layout': {
            'title': 'Income Vs Age Bubble Plot',
            'xaxis': {'title': 'Income'},
            'yaxis': {'title': 'Age'}
        }
    }
    return fig


def create_performance_graph(df):
    pass


def create_geographical_graph(df):
    pass


def create_default_scatter_plot(df):
    fig = {
        'data': [
            {'x': [0], 'y': [0], 'mode': 'markers', 'type': 'scatter'}
        ],
        'layout': {'title': 'Default Scatter Plot'}
    }
    return fig


@app.callback(
    Output('output-message', 'children'),
    Input('spec-radio', 'value'),
)
def update_output(specified_output):
    return f'Please upload the following: {specified_output}'


@app.callback(
    Output('loading', 'children'),
    [Input('upload-data', 'contents')],
    prevent_initial_call=True
)
def store_and_display_data(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded_content = base64.b64decode(content_string)
        df = pd.read_csv(StringIO(decoded_content.decode('utf-8')))

        db_connection = sqlite3.connect('uploaded_data.db')
        df.to_sql('uploaded_data_table', db_connection, if_exists='replace', index=False)
        db_connection.close()

        return f'Data uploaded and stored. Preview: {", ".join(df.columns)}'
    else:
        return 'No data uploaded.', None


if __name__ == "__main__":
    app.run_server(debug=True)
