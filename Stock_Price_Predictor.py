import yfinance as yf
import pandas as pd


# Primitive price predictions with markov chains...


def obtain_data(cutoff_date):
    """
    This function obtains the last 60 days worth of data from a given date.

    :param cutoff_date: Reference date for getting the prior 60 days data.
    :return: Dataframe containing the dates and correlated prices of the ASX200.
    """


def classify_data(df):
    """
    Adds another column to the data frame that contains the classifications of states relating to the data.

    :param df: Data frame to be processed.
    :return: Updated data frame that contains the state classifications.
    """


def get_transition_function(df):
    """
    Obtains the probabilities for state transitioning.
    Note: the order of probabilities correlate to [INCREASE, SAME, DECREASE].

    df: The data frame containing the state classifications (ie complete data frame).
    :return: Dictionary containing the states and their corresponding transition probabilities.
    """




