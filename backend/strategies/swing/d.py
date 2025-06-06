import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os

def plot_features(df,swing_highs,swing_lows,early_shifts, shifts_in_trend, ticker_symbol):
    plt.figure(figsize=(12, 6))
    # Convert detected swings to separate lists for plotting
    swing_high_times, swing_high_values = zip(*swing_highs) if swing_highs else ([], [])
    
    swing_low_times, swing_low_values = zip(*swing_lows) if swing_lows else ([], [])
    early_shifts_times, early_shifts_values = zip(*early_shifts ) if early_shifts else ([],[])
    shifts_in_trend_times, shifts_in_trend_values = zip(*shifts_in_trend) if shifts_in_trend else ([],[])
    # Plot the chart
    
    
    print("Swing High Times Length:", len(swing_high_times))
    print("Swing High Values Length:", len(swing_high_values))
    print("Swing Low Times Length:", len(swing_low_times))
    print("Swing Low Values Length:", len(swing_low_values))
    print("Early Shifts Times Length:", len(early_shifts_times))
    print("Early Shifts Values Length:", len(early_shifts_values))
    print("Shifts in Trend Times Length:", len(shifts_in_trend_times))
    print("Shifts in Trend Values Length:", len(shifts_in_trend_values))

    

    # Plot each candle
    for i in range(len(df)):
        color = 'green' if df['close'].iloc[i] >= df['open'].iloc[i] else 'red'  # Green for bullish, red for bearish
        # Plot the candle wicks (low to high)
        plt.plot([df['time'].iloc[i], df['time'].iloc[i]], [df['low'].iloc[i], df['open'].iloc[i]], color='black', linewidth=1)
        plt.plot([df['time'].iloc[i], df['time'].iloc[i]], [df['high'].iloc[i], df['close'].iloc[i]], color='black', linewidth=1)
        plt.plot([df['time'].iloc[i], df['time'].iloc[i]], [df['open'].iloc[i], df['close'].iloc[i]], color=color, linewidth=2)

    # Highlight swing highs and lows with markers
    plt.scatter(swing_high_times, swing_high_values, color='blue', marker='^', label='Swing Highs', s=100)
    plt.scatter(swing_low_times, swing_low_values, color='orange', marker='v', label='Swing Lows', s=100)
    plt.scatter(shifts_in_trend_times, shifts_in_trend_values, color='purple', marker='d', label='Early Shifts in Trend', s=100)
    plt.scatter(early_shifts_times, early_shifts_values, color='black', marker='8', label='Shifts in Trend', s=100)

    # Add chart labels and legend
    plt.title(f'Swing Highs and Lows for {ticker_symbol} from 2024-01-01 to 2024-09-30')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    
    save_dir = "plots"  # Directory to save the plot
    file_name = ticker_symbol+ ".png"
    # Ensure the directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Save the plot in the specified directory
    save_path = os.path.join(save_dir, file_name)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')  # dpi=300 for high quality
    plt.close()

    # Show the plot
    
    # plt.tight_layout()
    plt.show()



def fetch_historical_data(ticker_symbol,start,end,interval):
    # Fetch historical data for a specific ticker symbol
    ticker = yf.Ticker(ticker_symbol)
    historical_data = ticker.history(start=start, end=end, interval=interval)

    # Reset the index to make time a column
    historical_data.reset_index(inplace=True)

    dt_time_column_name = 'Date'
    if interval in ['1d', '5d', '1wk', '1mo', '3mo']:
        dt_time_column_name = "Date"
    else:
        dt_time_column_name='Datetime'

    df = pd.DataFrame({
    'time': historical_data[dt_time_column_name],
    'high': historical_data.High,
    'low': historical_data.Low,
    'open': historical_data.Open,
    'close': historical_data.Close,
    'volume': historical_data.Volume

    })
    
    return df



# Function to detect swing highs and lows based solely on close prices
def detect_swings(df, lookback=2):
    swing_highs = []
    swing_lows = []
    last_swing_high_index = -1
    last_swing_low_index = -1
    
    
    # -1 for downtrend , 1 for uptrend
    trend = 0
    
    

    highest_high_index = -1
    lowest_low_index =-1
    
    
    shifts_in_trend = []
    shift_in_trend_indices = []
    
    early_shifts = []
    
    # Start by marking the first point as a swing low
    swing_highs.append((df['time'].iloc[0], df['close'].iloc[0]))
    last_swing_high_index = 0
    highest_high_index = 0
    
    swing_lows.append((df['time'].iloc[0], df['close'].iloc[0]))
    last_swing_low_index = 0
    lowest_low_index = 0
    

    for i in range(lookback, len(df) - 0):#make this look back 0
        close = df['close'].iloc[i]

        # Check for swing high using only close prices
        prev_closes = df['close'].iloc[i - lookback:i]  # Close prices before current candle
        next_closes = df['close'].iloc[i + 1:i + lookback + 1]  # Close prices after current candle

        # if swing high
        if all(close > c for c in prev_closes) and all(close > c for c in next_closes):
            
            # print("made a swing high at ",close)
            # Only append swing high if there is a previous swing low
            # it is indeed a swing high
            last_swing_high_index = i
            swing_highs.append((df['time'].iloc[i], close))
            
            # we also need to see if this is the highest high
            
            if(highest_high_index==-1):
                # there was no higher high previously so we assign a higher high
                highest_high_index = i
                
            else:
                # there was a previous higher high which means if we breach that high
                # we also created a breach for uptrend so last swing low becomes guy responsible
                previous_highest_high =df['close'].iloc[highest_high_index]
                if(close>previous_highest_high):
                    
                    if(trend==0):
                        # trend was not set so we set the initial trend to uptrend
                        trend = 1
                        # last recent low becomes the guy responsible (lowest_low)
                        lowest_low_index = last_swing_low_index
                    elif trend ==1:
                        # trend was uptrend so we continue uptrend
                        # guy responsible shifts up
                        lowest_low_index = last_swing_low_index
                        pass
                    else:
                        # trend was downtrend so we change to uptrend
                        trend =1
                        # last recent low  becomes the guy responsible 
                        lowest_low_index = last_swing_low_index
                        shifts_in_trend.append((df['time'].iloc[i], df['close'].iloc[i]))
                        shift_in_trend_indices.append(i)
                        
                        # trend also shifts here
                        
                    # in all 3 cases - highest high changes to this swing high
                    highest_high_index = i
                    
                    

        # if swing low
        elif all(close < c for c in prev_closes) and all(close < c for c in next_closes):
            
            # print("made a swing low at ",close)
            # Only append swing low if there is a previous swing high
            #  and this is indeed a swing low
            last_swing_low_index = i
            swing_lows.append((df['time'].iloc[i], close))
            
            
            # we also need to see if this is the lowest low
            
            if(lowest_low_index==-1):
                # there was no lowest low previously so we assign a lowest low
                lowest_low_index = i
                
            else:
                # there was a previous lowest low which means if we breach that low
                # we also created a breach for downtrend so last swing high becomes guy responsible
                previous_lowest_low =df['close'].iloc[lowest_low_index]
                if(close<previous_lowest_low):
                    # print("also  made a breach for downtrend at ",close," trend is negative now")
                    
                    
                    if(trend==0):
                        # trend was not set so we set the initial trend to downtrend
                        trend = -1
                        # last recent high becomes the guy responsible (highest_high)
                        highest_high_index = last_swing_high_index
                    elif trend ==1:
                        # trend was uptrend so we change to downtrend
                        trend = -1
                        # last recent high  becomes the guy responsible
                        highest_high_index = last_swing_high_index
                        shifts_in_trend.append((df['time'].iloc[i], df['close'].iloc[i]))
                        shift_in_trend_indices.append(i)
                        # trend also shifts here
                    else:
                        # trend was downtrend so we change to downtrend
                        
                        # last recent high  becomes the guy responsible
                        highest_high_index = last_swing_high_index
                    
                
                    
                    # in all 3 cases lowest low shifts down
                    lowest_low_index=i
                
                    
                    
                    

        else:
            # merely a low / high
            # if close > prev close - it is high else it is low
            
            # now question is when does a trend change - 
            
            
            # in uptrend
            # if close is below guy responsible - we shift to possible downtrend - challenging
            # if close above, we dont care
            
            # in downtrend
            # if close above guy responsible - we shift to possible -uptrend - challenging
            # if close below, we dont care
            
            # how do we determine trend initially
            
            # if we make a lower low - we are in downtrend
            # if we make a higher high - we are in uptrend
            
            if(trend!=0):#atleast we have some trend
                
                if(trend==1): #we were in an uptrend
                    # if close is below guy responsible (lowest low)- we shift to possible downtrend - challenging lows
                    prev_low = df['close'].iloc[lowest_low_index]
                    if(close<prev_low):
                        # print("we are now challenging the lows after an uptrend")
                        early_shifts.append((df['time'].iloc[i], df['close'].iloc[i]))
                        shift_in_trend_indices.append(i)
                        # trend = -1
                        # highest_high_index = last_swing_high_index
                        # last_swing_low_index = i
                        
                        # # but what will become the lowest low in this case- unless there is a swing low we 
                        # # cant determine the lowest low - but let's for now make current close the lowest low
                        # lowest_low_index = i
                        
                        # shifts_in_trend.append((df['time'].iloc[i], df['close'].iloc[i]))
                elif trend==-1:
                    # we are in a downtrend
                    
                    # if close is above guy responsible - (highest high) 
                    # - we shift to possible uptrend - challenging highs
                    prev_high = df['close'].iloc[highest_high_index]
                    if(close>prev_high):
                        # print("we are now challenging the highs after a downtrend")
                        early_shifts.append((df['time'].iloc[i], df['close'].iloc[i]))
                        shift_in_trend_indices.append(i)
                        # trend = 1
                        # highest_high_index = i
                        # last_swing_high_index = i
                        # lowest_low_index = last_swing_low_index
                        # # shifts_in_trend.append((df['time'].iloc[i], df['close'].iloc[i]))
            
            # here we have used close to check if we are challenging guy responsible.
            # in the next version we can make it more concrete trend change by converting a close challenging guy responsible to 
            # maybe if in a downtrend we see a swing low being made above guy responsible then we can possibly confirm that trend has indeed changed 
            # on this time frame
                
            else:
                # print("No trend yet at ",close)
                pass
            
                        

    # return [swing_highs,swing_lows,early_shifts,shifts_in_trend,shift_in_trend_indices]
    # instead of returning these values plain and simple 
    # i also want to know about the territory that i am in
    if(trend==-1):
                                                                                            #trend, highest/lowest_point, guy-responsible  
        return [swing_highs,swing_lows,early_shifts,shifts_in_trend,shift_in_trend_indices,trend,lowest_low_index,highest_high_index]
    elif trend==1:
        return [swing_highs,swing_lows,early_shifts,shifts_in_trend,shift_in_trend_indices,trend,highest_high_index,lowest_low_index]
    else:
        return [swing_highs,swing_lows,early_shifts,shifts_in_trend,shift_in_trend_indices,trend,0,0]
    


symbol = "BTC-USD"
higher_tf = '1d'
start = "2024-09-01"
end = "2024-10-01"

# Fetch historical data
data = fetch_historical_data(ticker_symbol=symbol,start=start,end=end,interval=higher_tf)



# Run the swing detection function
swing_highs, swing_lows, early_shifts, shifts_in_trend, shift_in_trend_indices, trend, lowest_low_index, highest_high_index = detect_swings(data)

plot_features(data,swing_highs,swing_lows,early_shifts,shifts_in_trend,symbol)