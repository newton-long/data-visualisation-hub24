import dash
from dash import Dash, dcc, html, Output, Input, callback, State, ALL, callback_context
import dash_bootstrap_components as dbc
from Helper_Functions import *
from io import StringIO
from openai_function import chatbot

dash.register_page(__name__)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Chatbot", className='text-center'),
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Input(
                        id='input-box',
                        type='text',
                        placeholder='Talk to me here...',
                        value='',
                        style={'width': '100%', 'margin': '10px auto', 'padding': '10px', 'border-radius': '5px',
                               'border': '1px solid #ccc'}
                    ),
                ),
                dbc.Col(html.Button('Enter', id='enter-button', n_clicks=0,
                                    style={'padding': '10px', 'margin': '10px auto', 'border-radius': '5px'}))
            ]
        ),
        dbc.Row(
            dbc.Col(
                html.H5("Response will be below:", className='text-left')
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='output-container',
                         style={
                             'padding': '20px',
                             'background-color': '#f0f0f0',
                             'border': '1px solid #ccc',
                             'border-radius': '5px',
                             'font-size': '16px',
                             'width': '100%',
                             'margin': '20px auto',
                             'text-align': 'left'
                         }
                         )
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H2("Stock Price Predictor")
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Input(
                        id='prediction-input',
                        type='text',
                        placeholder='Enter the number of days into the future you want to predict...',
                        value='',
                        style={'width': '100%', 'margin': '10px auto', 'padding': '10px', 'border-radius': '5px',
                               'border': '1px solid #ccc'}
                    ),
                ),
                dbc.Col(html.Button('Generate Prediction Visual', id='prediction-button', n_clicks=0,
                                    style={'padding': '10px', 'margin': '10px auto', 'border-radius': '5px'}))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='prediction-vis', figure=default_graph())
                ),
            ]
        ),
    ]
)


# Use OpenAI api key or make you're own chatbot trained on primitive data...
@callback(
    Output('output-container', 'children'),
    [Input('enter-button', 'n_clicks')],
    [State('input-box', 'value')]
)
def update_output(n_clicks, input_text):
    if n_clicks:
        return f'Response: {chatbot(input_text)}'
    else:
        return ''
