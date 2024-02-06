import dash
from dash import Dash, dcc, html, Output, Input, callback, State, ALL, callback_context
import dash_bootstrap_components as dbc
from Helper_Functions import *
from io import StringIO

dash.register_page(__name__)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Talk to our chatbot !", className='text-center'),
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
                        value=''
                    ),
                )
            ]
        ),
        html.Button('Enter', id='enter-button', n_clicks=0),
        html.Div(id='output-container')
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
        return f'Processed text: {input_text}'
    else:
        return ''
