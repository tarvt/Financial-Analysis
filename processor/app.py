import json
import pandas as pd
import threading
import time
import redis
from flask import Flask
from prometheus_client import start_http_server, Gauge
from pyspark.sql import SparkSession 
from pyspark.streaming import StreamingContext 
from flask import Flask, jsonify
# Initialize Spark Session and Context 
spark = SparkSession.builder.appName("TradingIndicatorProcessor").getOrCreate() 
sc = spark.sparkContext 
ssc = StreamingContext(sc, 1) 
  
# DataFrame to store the processed data 
processed_data_df = pd.DataFrame() 
 
def select_appropriate_field(data): 
    if data['data_type'] == 'order_book': 
        return data['price'] 
    elif data['data_type'] == 'market_data': 
        return data['market_cap'] 
    # Add more conditions if other data types are relevant 
    else: 
        return None


# Initialize Redis client
redis_client = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)

# Create Prometheus metrics
ma_metric = Gauge('market_data_ma', 'Moving Average')
ema_metric = Gauge('market_data_ema', 'Exponential Moving Average')
rsi_metric = Gauge('market_data_rsi', 'Relative Strength Index')

def select_appropriate_field(data):
    if data['data_type'] == 'order_book':
        return data['price']
    elif data['data_type'] == 'market_data':
        return data['market_cap']
    # Add more conditions if other data types are relevant
    else:
        return None

def moving_average(series, periods=20):
    """
    Calculate the Moving Average (MA) for the given data.
    :param series: Pandas Series with numerical data.
    :param periods: Number of periods over which to calculate the average.
    :return: Pandas Series containing the moving averages.
    """
    return series.rolling(window=periods).mean()

def exponential_moving_average(series, periods=20):
    """
    Calculate the Exponential Moving Average (EMA) for the given data.
    :param series: Pandas Series with numerical data.
    :param periods: Number of periods over which to calculate the EMA.
    :return: Pandas Series containing the exponential moving averages.
    """
    return series.ewm(span=periods, adjust=False).mean()

def relative_strength_index(series, periods=14):
    """
    Calculate the Relative Strength Index (RSI) for the given data.
    :param series: Pandas Series with numerical data.
    :param periods: Number of periods over which to calculate the RSI.
    :return: Pandas Series containing the RSI values.
    """
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def stream_processed_data():
    series_dict = {
        'order_book': pd.Series(),
        'market_data': pd.Series(),
        # Add more as needed
    }

    while True:
        # Fetch data from Redis
        _, data = redis_client.blpop("processed_data") # Redis BLPOP command is used to remove and get the first element in a list, or block until one is available.
        data_dict = json.loads(data.decode('utf-8'))

        data_type = data_dict.get('data_type')
        if data_type in series_dict:
            value = select_appropriate_field(data_dict)
            if value is not None:
                series = series_dict[data_type]
                # Concatenate new value to the series
                new_series = pd.Series([value])
                series = pd.concat([series, new_series]).dropna()
                series_dict[data_type] = series

                # Perform calculations
                ma = moving_average(series)
                ema = exponential_moving_average(series)
                rsi = relative_strength_index(series)

                # Update Prometheus metrics
                ma_metric.set(ma.iloc[-1] if not ma.empty else None)
                ema_metric.set(ema.iloc[-1] if not ema.empty else None)
                rsi_metric.set(rsi.iloc[-1] if not rsi.empty else None)

                # Prepare and send data 
                processed_data = { 
                    'data_type': data_type, 
                    'MA': ma.iloc[-1] if not ma.empty else None, 
                    'EMA': ema.iloc[-1] if not ema.empty else None, 
                    'RSI': rsi.iloc[-1] if not rsi.empty else None 
                } 
                processed_data_clean = {k: (0 if pd.isna(v) else v) for k, v in processed_data.items()}
                # Send data to port 5005
                try: 
                    print(f"processed_data : {processed_data}")
                    #response = requests.post('http://0.0.0.0:5005/', json=json.dumps(processed_data))
                    #response = requests.post('http://0.0.0.0:5005/signal',  json=json.dumps(processed_data)) 
                    response = requests.post('http://0.0.0.0:5005/signal',  json=processed_data_clean) 
                    print(f"Data sent to port 5005: {processed_data}, Response: {response.text}") 
                except Exception as e: 
                    print(f"Error sending data: {e}") 
 

        time.sleep(1)

if __name__ == "__main__":
    # Start the Prometheus exporter
    start_http_server(9877)

    # Start streaming processed data
    threading.Thread(target=stream_processed_data).start()
