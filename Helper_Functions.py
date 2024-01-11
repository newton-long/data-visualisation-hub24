from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import sqlite3
import pandas as pd
import base64
import datetime
import io
import plotly.graph_objects as go
import numpy as np
import folium as fl
from io import BytesIO
import plotly.express as px
import plotly.figure_factory as ff

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


def convert_coordinates(coord_str):
    """
    Help convert to decimal values.
    :param coord_str:
    :return:
    """
    degrees, minutes, seconds = map(float, coord_str.split(':'))
    decimal_degrees = degrees + minutes/60 + seconds/3600
    return decimal_degrees


def create_high_tax_geo_bubble_plot(df):
    """
    Creates a figure that is geographical bubble plot...
    :param df: data frame required to plot the plot.
    :return: figure of the plot.
    """

    fig = px.scatter_mapbox(df,
                            lat='Latitude',
                            lon='Longitude',
                            size='Highest Average Taxable Income',
                            color='Highest Average Taxable Income',
                            center=dict(lat=-25.2744, lon=133.7751),
                            zoom=3,
                            mapbox_style="open-street-map")
    fig.update_layout(
        mapbox=dict(
            bearing=0,
            pitch=0,
            style='open-street-map'
        ),
        height=1000,  # Adjust the height
        width=2000,  # Adjust the width
    )

    return fig


def create_hexabin_graph(df):
    """
    Hexabin tryout -> something funky to mix it up against the bubble plot.
    :param df: Data to be used for the hexabin plot.
    :return: hexabin plot.
    """
    fig = ff.create_hexbin_mapbox(
        data_frame=df,
        lat="Latitude",
        lon="Longitude",
        nx_hexagon=40,
        opacity=0.6,
        labels={
            "color": "Highest Average Taxable Income",
        },
        # range_color=(df["Highest Average Taxable Income"].min(), df["Highest Average Taxable Income"].max()),
        # Set the range of color values
        mapbox_style="carto-positron",  # Experiment with different styles
        center=dict(lat=-25.2744, lon=133.7751),  # Centered over Australia
        zoom=3,  # Adjust the zoom level
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=800,  # Adjust the height
        width=1900,  # Adjust the width
    )

    return fig


# Proof of concept something more aesthetic... than the original data
def dummy_hexabin_plot():
    px.set_mapbox_access_token(open(".mapbox_token").read())
    np.random.seed(0)

    N = 500
    n_frames = 12
    lat = np.concatenate([
        np.random.randn(N) * 0.5 + np.cos(i / n_frames * 2 * np.pi) + 10
        for i in range(n_frames)
    ])
    lon = np.concatenate([
        np.random.randn(N) * 0.5 + np.sin(i / n_frames * 2 * np.pi)
        for i in range(n_frames)
    ])
    frame = np.concatenate([
        np.ones(N, int) * i for i in range(n_frames)
    ])

    fig = ff.create_hexbin_mapbox(
        lat=lat, lon=lon, nx_hexagon=15, animation_frame=frame,
        color_continuous_scale="Cividis", labels={"color": "Point Count", "frame": "Period"},
        opacity=0.5, min_count=1,
        show_original_data=True, original_data_marker=dict(opacity=0.6, size=4, color="deeppink")
    )
    return fig


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


def get_perf_data():
    db_connection = sqlite3.connect('performance_data.db')
    query = "SELECT * FROM performance_data_table"
    df = pd.read_sql(query, db_connection)
    db_connection.close()
    return df


def performance_line_graph(df):
    pass


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an CSV file
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


def populate_longitude_latitude(target, source, output):
    """
    Helper function to populate target CSV file that contains postcodes but no
    latitude and longitude values. Will extract from the source file that does contain those
    values, and then merge them into one singular dataframe and then save that dataframe as a
    new CSV file.
    :param output: name of the output (make sure to put .csv at the end of it)
    :param target: this is the target csv file that requires populating.
    :param source: csv file that contains the mother of all values.
    :return: new CSV file that has latitude and longitude values.
    """
    target_df = pd.read_csv(target)
    source_df = pd.read_csv(source)
    # Iterate and get all the postcode values... we use this to index
    for index, postcode in target_df['Postcode'].items():
        # Find the corresponding row in the source DataFrame based on 'Postcode'
        source_row = source_df[source_df['postcode'] == postcode]

        # Check if the 'Postcode' exists in the source DataFrame
        if not source_row.empty:
            # Extract latitude and longitude values from the source DataFrame
            latitude = source_row['lat'].iloc[0]
            longitude = source_row['long'].iloc[0]

            # Update the target DataFrame with latitude and longitude values
            target_df.at[index, 'Latitude'] = latitude
            target_df.at[index, 'Longitude'] = longitude

        # Save the modified DataFrame back to a new CSV file
    target_df.to_csv(output, index=False)


# populate_longitude_latitude("Data/Highest Average Taxable Income.csv",
#                             "Data/australian_meta_data.csv",
#                             "Data/Populated Highest Average Taxable Income.csv")
