from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import random
from strategies.change_in_trend_in_last_five import get_trends_data
import pandas as pd
from datetime import datetime
scrips_directory = "scrips/"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # Avoid unnecessary formatting



import json

# Open and read the JSON file
with open('form-options/form-options.json', 'r') as file:
    data = json.load(file)


intervals_supported = data["intervals"]
strategies = data["strategies"]
scrips = data["scrips"]



# Sample data for demonstration
stock_data = [
    {"name": "AAPL", "image": "https://via.placeholder.com/100?text=AAPL"},
    {"name": "GOOGL", "image": "https://via.placeholder.com/100?text=GOOGL"},
    {"name": "AMZN", "image": "https://via.placeholder.com/100?text=AMZN"},
    {"name": "MSFT", "image": "https://via.placeholder.com/100?text=MSFT"},
    {"name": "TSLA", "image": "https://via.placeholder.com/100?text=TSLA"},
    {"name": "FB", "image": "https://via.placeholder.com/100?text=FB"},
]


@app.route('/', methods=['post'])
def index():
    return "It works!"


@app.route('/api/stocks', methods=['POST'])
def get_stocks():
    # In a real scenario, you would use the input data from the request
    # For now, just return random stock data
    # num_stocks = random.randint(1, len(stock_data))  # Random number of stocks
    # selected_stocks = random.sample(stock_data, num_stocks)  # Randomly select stocks
    # return jsonify(selected_stocks)
    


    json_data = request.json  # Returns None if no JSON payload is sent
    if json_data:
        interval = json_data.get('interval')
        start_date_str = json_data.get('startDate')  # Example: '2024-10-22T12:30:00+00:00'
        end_date_str = json_data.get('endDate')      # Example: '2024-10-23T15:45:00+00:00'

        # Parse string to datetime with timezone info
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)

        # Remove timezone information (convert to naive datetime)
        start_date_naive = start_date.replace(tzinfo=None)
        end_date_naive = end_date.replace(tzinfo=None)
        scrip = json_data.get('scrip')
        strategy = json_data.get('strategy')
        
        if(start_date and end_date and scrip and strategy):
            if interval in intervals_supported:
                if scrip in scrips:
                    if strategy in strategies:
                        csv_path = scrips_directory+ str(scrips[scrip]["file"])
                        data = pd.read_csv(csv_path)
                        
                        n = data.shape[0]
                        final_list = []

                        for i in range(n):
                            ticker_symbol = data['Symbol'].iloc[i]
                            
                            ticker_symbol_altered = ticker_symbol+data['Extension'].iloc[i]
                            
                            
                            try:
                                [df,is_eligible,swing_highs,swing_lows,early_shifts,shift_in_trend_indices,trend,high_or_low_index,last_hope] =  get_trends_data(ticker_symbol_altered,start_date,end_date,interval)
                                if(is_eligible):
                                    # final_list.append(ticker_symbol)
                                    
                                    obj  = {}
                                    obj["name"]=ticker_symbol
                                    obj["image"]="https://via.placeholder.com/100?text=AAPL"
                                    obj["chart"]=json.loads(df.to_json(orient='index', indent=4))
                                    
                                    swing_high_indices = [i for (i,_) in swing_highs]
                                    
                                    swing_low_indices = [i for  (i,_) in swing_lows]
                                    early_shift_indices = [i for  (i,_) in early_shifts]
                                    obj["swing_highs"]=swing_high_indices
                                    obj["swing_lows"]=swing_low_indices
                                    obj["early_shifts"]=early_shift_indices
                                    obj["shift_in_trend"]=shift_in_trend_indices
                                    obj["trend"]=trend
                                    obj["high_or_low_index"]=high_or_low_index
                                    obj["last_hope"]=last_hope
                                    
                                    
                                    
                                    final_list.append(obj)
                                    
                                    
                                    
                            except Exception as e:
                                print(f"Error occurred for {ticker_symbol}",str(e))
                                
                        
                        
                        return jsonify(final_list)



                    else:
                        return jsonify({"error": "Invalid Strategy"}), 400
                else:
                    return jsonify({"error": "Invalid Scrip"}), 400
            else:
                return jsonify({"error": "Invalid Interval"}), 400
                
            
            
        else:
            return jsonify({"error": "Invalid input"}), 400
        
        
        
        
        



    






@app.route('/api/form-options', methods=['GET','POST'])
def get_screener_options():
    
    
    with open('form-options/form-options.json', 'r') as file:
        data = json.load(file)
        return json.dumps(data)
    

    


if __name__ == '__main__':
    
    try:
        app.run(port=8000,debug=True)
    
    except Exception as e:
        print("Exception occured: ",str(e))
