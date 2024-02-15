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
import random
from datetime import timedelta

"""
Helper functions for visualiser tool.
"""


def get_uploaded_data():
    """
    Reaches for 'uploaded_data.db' file and creates a df
    of all the data.

    :return: data frame from the uploaded data.
    """
    db_connection = sqlite3.connect('../uploaded_data.db')
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
    decimal_degrees = degrees + minutes / 60 + seconds / 3600
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
                            size='Average Taxable Income',
                            color='Average Taxable Income',
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
    :return: hexabin plot with individual data points.
    """
    # Create hexbin plot
    hexbin_fig = ff.create_hexbin_mapbox(
        data_frame=df,
        lat="Latitude",
        lon="Longitude",
        nx_hexagon=40,
        opacity=0.7,
        labels={"color": "Income"},
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        center=dict(lat=-25.2744, lon=133.7751),
        zoom=3,
    )

    # Create scatter plot for individual data points
    scatter_fig = go.Figure(go.Scattermapbox(
        lat=df["Latitude"],
        lon=df["Longitude"],
        mode='markers',
        marker=dict(
            size=8,
            color=df["Income"],
            colorscale="Viridis",
            opacity=0.7,
            colorbar=dict(title="Income"),
        ),
        hoverinfo='text',
        hovertext=df[["Latitude", "Longitude", "Income"]].astype(str).agg('<br>'.join, axis=1),
    ))

    # Combine the hexbin plot and scatter plot
    hexbin_fig.add_trace(scatter_fig.data[0])

    hexbin_fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=800,
        width=1900,
    )

    return hexbin_fig


# Proof of concept something more aesthetic... than the original data
def dummy_hexabin_data():
    # Set seed for reproducibility
    np.random.seed(42)

    # Number of data points
    n_points = 1000

    # Coordinates for Sydney, Australia
    location_lat = -33.8688
    location_lon = 151.2093

    # Generate random data around the specified location
    lat = np.random.normal(loc=location_lat, scale=0.05, size=n_points)
    lon = np.random.normal(loc=location_lon, scale=0.05, size=n_points)
    income = np.random.normal(loc=50000, scale=10000, size=n_points)  # Example: income

    # Create a DataFrame
    df = pd.DataFrame({
        'Latitude': lat,
        'Longitude': lon,
        'Income': income
    })

    # Save the data as a CSV file
    df.to_csv('Data/dummy_data_sydney.csv', index=False)


# dummy_hexabin_data()


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
    """
    This will track the closing balance at the end of each month...
    The idea is that overtime we can see which account has the most money within it...
    :param df: Data to be used...
    :return: Figure that shows the closing balances of different accounts over time...
    """
    # Create a line plot using Plotly Express with separate lines for each Account ID
    fig = px.line(df, x='EOM', y='ClosingBal', color='AcctId',
                  title='Closing Balances Over Time by Account ID',
                  labels={'EOM': 'Date', 'ClosingBal': 'Closing Balance', 'AcctId': 'Account ID'},
                  line_shape='linear', render_mode='svg')

    # Customize the layout
    fig.update_layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Closing Balance'),
        height=1200,  # Adjust the height as needed
        width=1700,  # Adjust the width as needed
        margin=dict(l=50, r=50, t=50, b=50),  # Adjust the margins to provide space around the plot
    )

    return fig


def text_output(df):
    """
    This function is to filter through the data given, to be able to distinguish the best
    performing account and thus which advisor was the best.
    :param df: the data to shift through.
    :return: Returns string associated with the best performing account... (COULD BE UPDATED TO SHOW ADVISOR)
    """
    # Iterate through each row and obtain the accountId and the corresponding closing balance
    bestAcc = None
    value = 0
    currAcc = None
    currValue = 0
    # Iterate through each row of the CSV file
    for index, row in df.iterrows():
        # The base case -> set the first account as the "best" as a reference point
        if bestAcc is None:
            bestAcc = row['AcctId']
            value = row['ClosingBal']
            continue
        if row['AcctId'] != bestAcc and currAcc is None:
            # Grab the last entry of the before closing balance
            value = df.iloc[index - 1]['ClosingBal'] - value
            # After the first account has been analysed we need to store the next account, ie
            # there must always be a pair at hand
            currAcc = row['AcctId']
            currValue = row['ClosingBal']
            # Now the next account is set we can con't
            continue
        # Below means that we've hit the next section
        if row['AcctId'] != currAcc:
            currValue = df.iloc[index - 1]['ClosingBal'] - currValue  # This will store the different
            # Once value is stored we compare
            if currValue > value:
                # If perform better than update the best account values
                value = currValue
                bestAcc = df.iloc[index - 1]['AcctId']
            # Else, we just continue
            currAcc = row['AcctId']
            currValue = row['ClosingBal']
            continue
        # Check if it is the last entry
        if index == df.index[-1]:
            # Update the current value
            currValue = row['ClosingBal'] - currValue
            # Now compare with the previous best account values
            if currValue > value:
                value = currValue
                bestAcc = row['AcctId']
    # It should naturally break out of the for loop
    # With the best account stored in the variables before...

    return f"1st: {bestAcc} with gain: {value}"


def worst_account(df):
    # Iterate through each row and obtain the accountId and the corresponding closing balance
    bestAcc = None
    value = 0
    currAcc = None
    currValue = 0
    # Iterate through each row of the CSV file
    for index, row in df.iterrows():
        # The base case -> set the first account as the "best" as a reference point
        if bestAcc is None:
            bestAcc = row['AcctId']
            value = row['ClosingBal']
            continue
        if row['AcctId'] != bestAcc and currAcc is None:
            # Grab the last entry of the before closing balance
            value = df.iloc[index - 1]['ClosingBal'] - value
            # After the first account has been analysed we need to store the next account, ie
            # there must always be a pair at hand
            currAcc = row['AcctId']
            currValue = row['ClosingBal']
            # Now the next account is set we can con't
            continue
        # Below means that we've hit the next section
        if row['AcctId'] != currAcc:
            currValue = df.iloc[index - 1]['ClosingBal'] - currValue  # This will store the different
            # Once value is stored we compare
            if currValue < value:
                # If perform better than update the best account values
                value = currValue
                bestAcc = df.iloc[index - 1]['AcctId']
            # Else, we just continue
            currAcc = row['AcctId']
            currValue = row['ClosingBal']
            continue
        # Check if it is the last entry
        if index == df.index[-1]:
            # Update the current value
            currValue = row['ClosingBal'] - currValue
            # Now compare with the previous best account values
            if currValue < value:
                value = currValue
                bestAcc = row['AcctId']
    # It should naturally break out of the for loop
    # With the best account stored in the variables before...

    return f"last: {bestAcc} with gain: {value}"


# Fake data generator for the sales demonstration
def generate_sample_sales_data(file_path='sample_sales_data.xlsx', num_rows=30):
    """
    Generate sample sales data and save it to an Excel file.

    Parameters:
    - file_path (str): Path to the Excel file where the data will be saved.
    - num_rows (int): Number of rows (entries) to generate in the dataset.

    Returns:
    - None
    """
    data = {
        'Date': pd.date_range(start='2022-01-01', periods=num_rows, freq='D'),
        'Product': [f'Product_{random.randint(1, 5)}' for _ in range(num_rows)],
        'Category': [f'Category_{random.choice(["A", "B", "C"])}' for _ in range(num_rows)],
        'Sales': [random.randint(100, 500) for _ in range(num_rows)],
    }

    sales_df = pd.DataFrame(data)

    # Save the data to an Excel file
    sales_df.to_excel(file_path, index=False)

    print(f"Sample sales data saved to '{file_path}'")


# generate_sample_sales_data(file_path='custom_sales_data.xlsx', num_rows=50)


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

# Below is some self-made advisor performance data, to show proof of concept, since actual data given was impossible
# to extrapolate from
def generate_and_save_sample_data(num_entries=365, output_csv='sample_data.csv'):
    """
    Generate sample data with dates, advisor IDs, and returns, and save it to a CSV file.

    Parameters:
    - num_entries (int): Number of entries to generate.
    - output_csv (str): File path to save the CSV file.

    Returns:
    - pd.DataFrame: DataFrame with columns for Date, AdvisorID, and Returns.
    """
    start_date = pd.to_datetime('2022-01-01')
    end_date = start_date + timedelta(days=num_entries - 1)

    # Generate random advisor IDs
    advisor_ids = [random.randint(1, 5) for _ in range(num_entries)]  # Assume 5 advisors

    # Generate random returns in dollars
    returns = [random.uniform(-1000, 1000) for _ in range(num_entries)]

    # Create DataFrame
    data = {'Date': pd.date_range(start=start_date, end=end_date, freq='D'),
            'AdvisorID': advisor_ids,
            'Returns': returns}
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
    print(f"Sample data saved to '{output_csv}'")

    return df


def get_spider_data():
    """
    Reaches for 'uploaded_data.db' file and creates a df
    of all the data.

    :return: data frame from the uploaded data.
    """
    db_connection = sqlite3.connect('sales_spider.db')
    query = "SELECT * FROM sales_data_table"
    df = pd.read_sql(query, db_connection)
    db_connection.close()
    return df


# May add in date slider and can see the portfolio change over time
# Also add the advisor number etc basic implementation, would look really nice actually...
def sales_spider(df, adviser):
    """
    Filters through the data frame, obtains enough information about the asset composition,
    then return the figure that shows that...
    :param adviser: The code corresponding to the advisor button that was pressed.
    :param df: data frame to be filtered with
    :return: spider graph from the asset composition
    """
    # Need to filter and count the data entries, to store the number of specific of one asset there is
    # And the different type of asset classes... -> build two lists, and dynamically append one by one
    # Initialize empty lists to store asset classes and their counts
    asset_classes = []
    class_counts = []

    filtered = df[df['adviserCode'] == adviser]
    # Iterate through each row in the 'AssetClass' column
    for asset_class in filtered['AssetClass']:
        # Check if the asset class is already in the list
        if asset_class not in asset_classes:
            # If not, add it to the list of asset classes
            asset_classes.append(asset_class)
            # Count the occurrences of the asset class in the DataFrame and add it to the counts list
            class_counts.append(filtered[filtered['AssetClass'] == asset_class].shape[0])

    fig = go.Figure(data=go.Scatterpolar(
        r=class_counts,
        theta=asset_classes,
        fill='toself'
    ))

    return fig


def get_advisor_value(data):
    """
    Passes in the data and obtains the value of the advisor that is managing this set of data.
    :param data: The data frame relating to the spider graph.
    :return: The advisor code for this asset portfolio.
    """
    advisor = data['adviserCode'][0]

    return advisor


def sales_bar(data, adviser):
    """
    This function outputs a bar graph summarising the total market value of the aggregated asset classes.
    :param adviser: The code corresponding to the advisor button that was pressed.
    :param data: The data frame associated with the particular advisor.
    :return: A bar graph that shows us the market value of the asset classes aggregated.
    """
    # Initialize empty lists to store asset classes and their aggregated market values
    asset_classes = []
    market_values = []

    # Filter the filter
    filtered = data[data['adviserCode'] == adviser]
    # Iterate through unique asset classes
    for asset_class in filtered['AssetClass'].unique():
        # Filter data for the current asset class
        filtered_data = filtered[filtered['AssetClass'] == asset_class]
        # Sum the market values for the current asset class
        total_market_value = filtered_data['MarketValue'].sum()
        # Append the asset class and its total market value to the lists
        asset_classes.append(asset_class)
        market_values.append(total_market_value)

    # Create the bar graph
    fig = go.Figure(go.Bar(
        x=asset_classes,
        y=market_values
    ))

    # Customize the layout
    fig.update_layout(
        title='Total Market Value by Asset Class',
        xaxis_title='Asset Class',
        yaxis_title='Total Market Value',
        bargap=0.1,  # Gap between bars
        bargroupgap=0.2,  # Gap between groups of bars
        xaxis_tickangle=-45  # Rotate x-axis labels for better readability
    )

    return fig


# Possibly write script to filter the original excel sheet, get and save a bunch as each chunk and keep
# uploading different ones... could be very effective to show case the potential at least


def sales_spider_2():
    fig = go.Figure(data=go.Scatterpolar(
        r=[4, 3, 2, 5, 1],
        theta=['c', 'l', 'o', 's', 'e', 'r'],
        fill='toself'
    ))

    return fig


# # Example usage: generate_and_save_sample_data()
# sample_data = generate_and_save_sample_data(num_entries=365)
#
# # Visualization: Line chart - Returns over time, each advisor has a separate line
# fig = px.line(sample_data, x='Date', y='Returns', color='AdvisorID',
#               title='Returns Over Time by AdvisorID')
# fig.show()


def aggregate_closing_bal_and_save(csv_output_path, excel_input_path):
    # Read the Excel file into a DataFrame
    df_excel = pd.read_excel(excel_input_path, "Performance")

    # Group by 'Advisor' and 'Date' and sum the 'Market Value' for each combination
    df_aggregated = df_excel.groupby(['AcctId', 'EOM'])['ClosingBal'].sum().reset_index()

    # Save the aggregated DataFrame to a new CSV file
    df_aggregated.to_csv(csv_output_path, index=False)


# aggregate_closing_bal_and_save("Data/performance_extract.csv",
#                                "Data/2023-11-22 - Sample Data for Visualisations.xlsx")

# def advisor_performance_data_extraction():
#     # Open desired excel sheet
#     df = pd.read_excel("Data/2023-11-22 - Sample Data for Visualisations.xlsx")
#     # Loop through each row and sum up the market value of all assets for that one row
#
#     # Store that cumulative row into a new csv file...

def create_sales_funnel_chart():
    data = pd.DataFrame(dict(
        Pipeline=["Cold Outreach", "Qualified Leads", "Demo Calls Booked", "Closed",
                  "Cold Outreach", "Qualified Leads", "Demo Calls Booked", "Closed",
                  "Cold Outreach", "Qualified Leads", "Demo Calls Booked", "Closed",
                  "Cold Outreach", "Qualified Leads", "Demo Calls Booked", "Closed"],
        x=[97, 70, 40, 20,
           60, 40, 20, 5,
           100, 60, 20, 10,
           200, 150, 100, 50],
        Locations=["Brisbane", "Brisbane", "Brisbane", "Brisbane",
                   "Gold Coast", "Gold Coast", "Gold Coast", "Gold Coast",
                   "Melbourne", "Melbourne", "Melbourne", "Melbourne",
                   "Sydney", "Sydney", "Sydney", "Sydney"],
    ))
    fig = px.funnel(data, x='x', y='Pipeline', color='Locations')

    return fig
