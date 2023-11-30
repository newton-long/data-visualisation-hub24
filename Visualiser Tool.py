"""
Controls the database, and it's relation with the front-end (js).
Store the data here.
"""

import sqlite3
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from bubble_plot.bubble_plot import bubble_plot

# There are 3 main data sets to be uploaded...
# 1) income by age
# 2) income by state (geographical view)
# 3) Benchmark based on ROI

# csvFilePath = 'Data/2021 Male Incomes Across Age Groups.csv'
#
# rowsToRead = 17
# colsToRead = 11
# df = pd.read_csv(csvFilePath, nrows=rowsToRead, usecols=range(colsToRead))
# # ADD OTHER 2 DATA FRAMES... BUT RN WE WORK WITH JUST ONE
#
# # Connect the data frame to sql lite
# con = sqlite3.connect('age_income.db')
# tableName = 'age_income_table'
#
# df.to_sql(tableName, con, index=False, if_exists='replace')
#
# query = "SELECT * FROM age_income_table"
# # Extract data from the data base
# data = pd.read_sql_query(query, con)
# # Close after extracting data from the database
# con.close()

sns.set_style("darkgrid")
dff = pd.read_csv("Data/Incomes vs Age.csv")
bubble_plot(dff, x='Age Range', y='3500 or more')
plt.show()

# xValues = data.iloc[1:rowsToRead - 2, 0].values
# yValues = data.iloc[0, 1:colsToRead - 2].values
# # Extracts the actual population values in array form...
# values = data.iloc[1:rowsToRead - 2, 1:colsToRead - 2].values




