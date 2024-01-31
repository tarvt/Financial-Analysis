import logging 
import json 
from pyspark import SparkContext 
from pyspark.streaming import StreamingContext 
from flask import Flask, jsonify 
 
app = Flask(__name__) 
 
received_logger = logging.getLogger('received_data') 
received_logger.setLevel(logging.INFO) 
received_handler = logging.FileHandler('received.log') 
received_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') 
received_handler.setFormatter(received_formatter) 
received_logger.addHandler(received_handler) 
validated_logger = logging.getLogger('validated_data') 
validated_logger.setLevel(logging.INFO) 
validated_handler = logging.FileHandler('validated.log') 
validated_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') 
validated_handler.setFormatter(validated_formatter) 
validated_logger.addHandler(validated_handler) 
 
# Initialize Spark Streaming context with a batch interval of 1 second 
sc = SparkContext("local[2]", "DataIngestor") 
ssc = StreamingContext(sc, 1) 
 
# Create a DStream that listens to a socket on port 5000 for incoming data 
data_stream = ssc.socketTextStream("172.18.0.0", 5000) 
 # Initialize latest_validated_data with a default value 
latest_validated_data = {"message": "No validated data available"}
def validate_data(data): 
    # Check if the data is a dictionary (JSON object) 
    if not isinstance(data, dict): 
        return False 
 
    # Define the required fields for each data type 
    required_fields = { 
        "economic_indicator": ["indicator_name", "timestamp", "value"], 
        "news_sentiment": ["sentiment_magnitude", "sentiment_score", "stock_symbol", "timestamp"], 
        "order_book": ["order_type", "price", "quantity", "stock_symbol", "timestamp"], 
        "market_data": ["market_cap", "pe_ratio", "stock_symbol", "timestamp"] 
    } 
 
    # Check if the "data_type" field is present in the data 
    if "data_type" not in data: 
        return False 
 
    # Get the list of required fields for the data type 
    required_fields_for_type = required_fields.get(data["data_type"]) 
 
    # If the data type is not recognized, return False 
    if not required_fields_for_type: 
        return False 
 
    # Check if all the required fields are present in the data 
    for field in required_fields_for_type: 
        if field not in data: 
            return False 
 
    # Additional custom validation logic can be added here if needed 
 
    # If all checks pass, return True to indicate valid data 
    return True
 
def process_data(rdd):  
    global latest_validated_data  
    try:  
        # Extract the data from the RDD  
        data = rdd.collect() 
        print(data)  
        for item in data: 
            # Convert the string representation of a dictionary to an actual dictionary 
            try: 
                item_dict = json.loads(item.replace("'", "\"")) 
            except json.JSONDecodeError: 
                # If json.loads fails, use eval as a fallback 
                # Be cautious with eval, it's a potential security risk 
                item_dict = eval(item) 
 
            received_logger.info(f"Received data: {item_dict}")  
            if validate_data(item_dict):  
                validated_logger.info(f"Validated data: {item_dict}")  
                latest_validated_data = item_dict  
            else:  
                logging.error(f"Corrupted data: {item_dict}")  
    except Exception as e:  
        logging.error(f"Error processing data: {str(e)}")
        
# Process the data stream 
data_stream.foreachRDD(process_data) 
@app.route('/') 
def get_validated_data(): 
    global latest_validated_data 
    return jsonify(latest_validated_data)
 
if __name__ == '__main__': 
    try: 
        ssc.start() 
        app.run(host='0.0.0.0', port=5002) 
        ssc.awaitTermination() 
    except Exception as e: 
        logging.critical(f"Fatal error: {e}")
