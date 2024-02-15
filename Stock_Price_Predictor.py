import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import random


# Primitive price predictions with markov chains...


def obtain_data():
    """
    This function obtains the last 60 days worth of data from the present day.

    :return: Dataframe containing the dates and correlated prices of the ASX200 60 days prior to present day.
    """
    ticker_symbol = "^AXJO"

    # Get today's date
    end_date = datetime.today().strftime('%Y-%m-%d')

    # Calculate the date 60 days ago
    start_date = (datetime.today() - timedelta(days=60)).strftime('%Y-%m-%d')

    # Fetch historical data from Yahoo Finance
    asx200_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    # Reset index to make 'Date' a regular column
    asx200_data.reset_index(inplace=True)

    # Keep only the 'Date' and 'Close' columns
    asx200_data = asx200_data[['Date', 'Close']]

    return asx200_data


def classify_data(df):
    """
    Adds another column to the data frame that contains the classifications of states relating to the data.

    :param df: Data frame to be processed.
    :return: Updated data frame that contains the state classifications.
    """
    df['State'] = 'SAME'

    # Classify states based on price changes compared to the previous day
    for i in range(1, len(df)):
        if df.loc[i, 'Close'] > df.loc[i - 1, 'Close']:
            df.loc[i, 'State'] = 'INCREASE'
        elif df.loc[i, 'Close'] < df.loc[i - 1, 'Close']:
            df.loc[i, 'State'] = 'DECREASE'

    return df


def get_transition_function(df):
    """
    Obtains the probabilities for state transitioning.
    Note: the order of probabilities correlate to [INCREASE, SAME, DECREASE].

    df: The data frame containing the state classifications (i.e., complete data frame).
    :return: List containing the transition probabilities in the order [INCREASE, SAME, DECREASE].
    """
    transitions = {'INCREASE': 0, 'SAME': 0, 'DECREASE': 0}

    # Iterate through all days except the last one
    for i in range(len(df) - 1):
        current_state = df.iloc[i]['State']
        next_state = df.iloc[i + 1]['State']

        # Determine the type of transition
        if next_state > current_state:
            transitions['INCREASE'] += 1
        elif next_state == current_state:
            transitions['SAME'] += 1
        else:
            transitions['DECREASE'] += 1

    # Calculate transition probabilities
    total_transitions = sum(transitions.values())
    transition_probabilities = [count / total_transitions for count in transitions.values()]

    return transition_probabilities


def predict_future_values(transition_func, last_60_days, days):
    """
    Predict future closing values based on the transition probabilities.

    :param transition_func: List of transition probabilities for state prediction.
    :param last_60_days: Closing values of the last 60 days.
    :param days: Number of days into the future to predict.
    :return: Predicted closing values for the future days.
    """
    predicted_values = []

    # Initialize the current value as the last value from the training data
    current_value = last_60_days[-1]

    # Predict future values based on the transition probabilities
    for _ in range(days):
        # Determine the next state based on transition probabilities
        next_state_index = predict_state_index(transition_func)
        next_state = ['INCREASE', 'SAME', 'DECREASE'][next_state_index]

        # Determine the next value based on the predicted state
        if next_state == 'INCREASE':
            current_value += 5
        elif next_state == 'DECREASE':
            current_value -= 5

        # Append the predicted value to the list
        predicted_values.append(current_value)

        # Update the last 60 days with the new value
        last_60_days = last_60_days[1:] + [current_value]

    return predicted_values


def predict_state_index(transition_probabilities):
    """
    Predict the next state index based on the transition probabilities.

    :param transition_probabilities: List of transition probabilities.
    :return: Index of the predicted state.
    """
    # If the first state is 'SAME', set its probability to 1 and adjust other probabilities accordingly
    transition_probabilities = [1] + [prob / (len(transition_probabilities) - 1) for prob in transition_probabilities[1:]]
    # Randomly choose the next state index based on transition probabilities
    return random.choices(range(len(transition_probabilities)), weights=transition_probabilities)[0]


def prediction_graph(days, transition_func, df):
    """
    Generate a prediction visualization for a given number of days into the future.

    :param days: Number of days into the future to predict.
    :param transition_func: Transition function for state prediction.
    :param df: DataFrame containing the training data.
    :return: Plotly Figure object containing the prediction visualization.
    """
    # Plot the training data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Training Data'))

    # Predict and plot future values
    future_dates = pd.date_range(start=df['Date'].iloc[-1], periods=days)
    future_values = predict_future_values(transition_func, df['Close'].values[-60:], days)
    fig.add_trace(go.Scatter(x=future_dates, y=future_values, mode='lines', name='Predicted Values'))

    # Customize plot layout
    fig.update_layout(title='Prediction Visualization',
                      xaxis_title='Date',
                      yaxis_title='Closing Value')

    return fig
