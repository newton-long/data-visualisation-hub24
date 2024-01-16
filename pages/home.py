import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Output, Input, callback, State
import base64
import sqlite3
from io import StringIO
from Helper_Functions import *

dash.register_page(__name__, path="/")


layout = dbc.Container(
    [
        dcc.Location(id="home-url", refresh=False),
        # Leading row
        dbc.Row(
            [
                # Put a col in
                dbc.Col(
                    html.H1("Data Visualisation Tool", className='text-center'),
                ),
            ]
        ),
        # Row that contains description of what to do
        dbc.Row(
            dbc.Col(
                dcc.Markdown("Please upload your data. "
                             "[CLICK HERE for GitHub README]"
                             "(https://github.com/newton-long/data-visualisation-hub24)"),
            ),
            className='mb-4',
        ),
        # Row for the upload button
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
                    html.Div(id='upload-status')
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    # Add a Divider to aggregate components together
                    html.Div([
                        html.P("Select output:"),
                        dcc.RadioItems(
                            id='spec-radio',
                            options=[
                                {'label': ' Weekly Income Vs Age', 'value': 'Income vs age data for bubble '
                                                                            'chart output.'},
                                {'label': ' Taxable Income Bubble Plot', 'value': 'Post code & Taxable Income'},
                                {'label': ' Taxable Income Hexabin Plot', 'value': 'Hexabin version of above'},
                            ],
                            value='After uploading your data, please select the corresponding output:',
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
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='visualisation', figure=default_graph())
                ),
            ]
        ),
    ],
    fluid=True,
)


@callback(
    # Output
    Output('upload-status', 'children'),
    Input('upload-data', 'contents'),
    prevent_initial_call=True
)
def store_data(contents):
    """
    When the user uploads data (CSV), this will update the graph and also
    let the user know if data was properly uploaded.

    :param contents: Preview of the data (some columns).
    :return: Display of graph and upload success.
    """
    # Check if the contents exists or not -> indicative whether something was uploaded
    upload_status = []
    content_type, content_string = contents.split(',')
    decoded_content = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded_content.decode('utf-8')))
    # Currently just going to be one singular .db file -> assuming need to upload each time...
    db_connection = sqlite3.connect('../uploaded_data.db')
    df.to_sql('uploaded_data_table', db_connection, if_exists='replace', index=False)
    db_connection.close()
    # Shows the upload status when user uploads a file
    upload_status.append(f"CSV successfully uploaded and stored ✅.")

    return upload_status


@callback(
    # Output message for which radio item is selected
    [
        Output('output-message', 'children'),
        Output('visualisation', 'figure')
    ],
    [
        Input('spec-radio', 'value'),
    ],
    prevent_initial_call=True
)
def update_output(selected_radio):
    # Dependent on which radio is selected, output specific graph (only if compatible data provided)
    graph = None
    # Obtain the data frame
    data = get_uploaded_data()
    if data is not None:
        # Three possible outputs (the outputs do not update dynamically, small functional flaw)
        if selected_radio == "Income vs age data for bubble chart output.":
            graph = create_bubble_plot(data)
        elif selected_radio == "Post code & Taxable Income":
            graph = create_high_tax_geo_bubble_plot(data)
        elif selected_radio == "Hexabin version of above":
            graph = create_hexabin_graph(data)
        return "Data uploaded 😊!", graph
    # If no data has been uploaded then let the user know
    else:
        return "No data uploaded ❌!", None

