from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import sqlite3
import pandas as pd
import base64
import datetime
import io
import plotly.graph_objects as go
import numpy as np

"""
Helper functions for visualiser tool.
"""


def get_uploaded_data():
    """
    Reaches for 'uploaded_data.db' file and creates a df
    of all the data.

    :return: data frame from the uploaded data.
    """
    db_connection = sqlite3.connect('uploaded_data.db')
    query = "SELECT * FROM uploaded_data_table"
    df = pd.read_sql(query, db_connection)
    db_connection.close()
    return df


def create_bubble_plot(df):
    """
    Bubble plot specific output.

    :param df: data frame that contains necessary data for bubble output.
    :return: bubble plot.
    """
    colors = np.arange(len(df))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df['Income'],
            y=df['Age'],
            mode='markers',
            marker=dict(
                size=df['Size'],
                color=colors,
                colorscale='Viridis',
                colorbar=dict(title='Age (lighter colour = older)')
            )
        )
    )

    fig.update_layout(
        title='Weekly Income Vs Age: Bubble Plot',
        xaxis=dict(title='Income (0 - ..., ... - ..., to 3500+)', range=None),
        yaxis=dict(title='Age (0 - 20, 20 - 40, ...).', range=None),
        width=1600,
        height=800,
    )

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


def default_graph():
    # Define coordinates for a smiley face
    data = {
        'X': [2, 8, 5, 5],
        'Y': [6, 6, 4, 2]
    }
    # Create a Plotly scatter plot
    fig = go.Figure()
    # Set axis limits
    fig.update_xaxes(range=[0, 10])
    fig.update_yaxes(range=[0, 8])

    # Add labels
    fig.update_layout(xaxis_title='EMPTY GRAPH', yaxis_title='EMPTY GRAPH')

    return fig


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


def convert_csv_json(csv_file, json_file):
    """
    Lil helper function to convert any CSV files to JSON files for javascript usage,
    as data for back-end for js applications...

    :param csv_file: file path name of the csv desired for conversion.
    :param json_file: output file path name for the JSON output.
    :return: None, will create and save JSON file in specified location.
    """
    try:
        df = pd.read_csv(csv_file)

        df.to_json(json_file, orient='records', lines=True)

        print(f"Conversion success. JSON file saved to: {json_file}")

    except Exception as e:
        print(f"Error: {e}")
