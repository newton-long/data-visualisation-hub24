import dash
from dash import Dash, dcc, html, Output, Input, callback, State
import dash_bootstrap_components as dbc
from Helper_Functions import *

dash.register_page(__name__)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Sales Data Visualisations", className='text-center'),
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                html.P(
                    "Welcome to our Sales Data Visualizations page! Discover insights and trends through dynamic "
                    "visualizations of your sales data."
                    "In addition to exploring the data, we also want to empower you with effective selling practices. "
                    "Successfully selling a product or service involves a combination of understanding your offering, "
                    "your target audience,"
                    "and developing strong communication skills. We believe in building long-term relationships, "
                    "providing value to our customers,"
                    "and upholding the highest standards of ethics and integrity in all our interactions. Explore our "
                    "visualizations and learn more about"
                    "how to enhance your sales effectiveness!"
                ),
            ),
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H2("Featured Visualizations", className='text-center'),
                    className='mb-4'
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='sales-line-chart',
                        figure=default_graph(),
                        # Replace with your actual function to generate line chart data
                    ),
                    className='mb-4'
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='sales-pie-chart',
                        figure=default_graph(),
                        # Replace with your actual function to generate pie chart data
                    ),
                    className='mb-4'
                ),
            ]
        ),
        # Add more visualizations as needed
    ]
)
