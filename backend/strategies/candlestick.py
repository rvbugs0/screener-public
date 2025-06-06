import pandas as pd
import mplfinance as mpf

# Load the CSV data into a DataFrame
df = pd.read_csv('abc.csv', parse_dates=['Date'], index_col='Date')

# Prepare the data for the candlestick chart
candlestick_data = df[['Open', 'High', 'Low', 'Close']]

# Plot the candlestick chart
mpf.plot(candlestick_data, type='candle', style='charles', title='Candlestick Chart',
         ylabel='Price', volume=False)
