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
                    html.H1("Sales Data Visualisations", className='text-center'),
                ),
            ]
        ),
        dbc.Row(
            dbc.Col([
                html.P("Sales data for this month:")
            ]),
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='funnel-chart',
                    figure=create_sales_funnel_chart()
                        )
                )
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.H2("Asset Portfolio Visualisations", className='text-center',
                            style={'padding-top': '20px'}
                            ),
                    className='mb-4'
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Upload(
                        id='upload-sales',
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
                    html.Div(id='sales-upload', children='Upload status will be displayed here.')
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='advisors', style={'margin-top': '20px'}, children=[])
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='advisor-detail', children='Advisor Number will be here.',
                             style={'margin-top': '20px'})
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
                        id='sales-bar-graph',
                        figure=default_graph(),
                    ),
                    className='mb-4'
                ),
            ]
        )
    ]
)


# This callback, upon upload will automatically create the advisor buttons per advisor code...
# Then with these same buttons they each will have a dynamic id...
@callback(
    [
        Output('sales-upload', 'children'),
        Output('advisors', 'children')
    ],
    Input('upload-sales', 'contents'),
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
        db_connection = sqlite3.connect('sales_spider.db')
        df.to_sql('sales_data_table', db_connection, if_exists='replace', index=False)
        db_connection.close()

        # At this point create the list of all possible advisor buttons
        data = get_spider_data()
        advisorCodes = data['adviserCode'].unique()
        # For demonstration purposes, let's assume the upload was successful
        return ('File successfully uploaded 😊. Select an adviser code to view portfolio:',
                [
                    html.Button(str(codes),
                                id={'type': 'advisor-button', 'index': str(codes)},
                                style={'margin-top': '10px', 'border-radius': '8px'},
                                n_clicks=0)
                    for codes in advisorCodes
                ])
    else:
        return 'No file uploaded 🙁.'


@callback(
    [Output('sales-line-chart', 'figure'),
     Output('advisor-detail', 'children'),
     Output('sales-bar-graph', 'figure')
     ],
    Input({'type': 'advisor-button', 'index': '1201'}, 'n_clicks'),
    State({'type': 'advisor-button', 'index': '1201'}, 'n_clicks'),
    prevent_initial_call=True
)
def update_output(n_clicks, state_clicks):
    # Obtain the data frame
    data = get_spider_data()
    # Unable to filter which code was chosen
    advisor = "Advisor Code of this Portfolio: " + str(1201)
    if n_clicks is not None:
        return sales_spider(data, 1201), advisor, sales_bar(data, 1201)
    return None, "", None
