import json 
import pandas as pd 
import threading 
import time 
import requests 
from pyspark.sql import SparkSession 
from pyspark.streaming import StreamingContext 
 
# Initialize Spark Session and Context 
spark = SparkSession.builder.appName("TradingIndicatorProcessor").getOrCreate() 
sc = spark.sparkContext 
ssc = StreamingContext(sc, 1) 
 
# DataFrame to store the processed data 
processed_data_df = pd.DataFrame() 
 
# Function to calculate Moving Average 
def moving_average(data, periods=20): 
    return data['value'].rolling(window=periods).mean() 
 
# Function to calculate Exponential Moving Average 
def exponential_moving_average(data, periods=20): 
    return data['value'].ewm(span=periods, adjust=False).mean() 
 
# Function to calculate Relative Strength Index 
def relative_strength_index(data, periods=14): 
    delta = data['value'].diff() 
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean() 
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean() 
    rs = gain / loss 
    return 100 - (100 / (1 + rs)) 
 
# Function to process each RDD 
def process_data(rdd): 
    global processed_data_df 
    if not rdd.isEmpty(): 
        df = rdd.toDF().toPandas() 
        print(f"Received data: {df}") 
        df['MA'] = moving_average(df) 
        df['EMA'] = exponential_moving_average(df) 
        df['RSI'] = relative_strength_index(df) 
        processed_data_df = processed_data_df.append(df) 
 
# Function to stream processed data 
def stream_processed_data(): 
    while True: 
        if not processed_data_df.empty: 
            data_to_send = processed_data_df.iloc[0].to_json() 
            processed_data_df.drop(processed_data_df.index[0], inplace=True) 
            print(f"Data to send: {data_to_send}") 
            try: 
                requests.post('http://127.0.0.1:5004/', json=json.loads(data_to_send)) 
            except Exception as e: 
                print(f"Error sending data: {e}") 
            time.sleep(1) 
 
# Create a DStream that listens to a socket on port 5002 for incoming data 
data_stream = ssc.socketTextStream("localhost", 5002) 
data_stream.foreachRDD(process_data) 
 
# Start the Spark Streaming Context 
ssc.start() 
 
# Run the streaming function in a separate thread 
threading.Thread(target=stream_processed_data).start() 
 
ssc.awaitTermination()