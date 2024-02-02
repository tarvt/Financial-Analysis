import logging 
import json 
import socket 
from pyspark import SparkContext 
from pyspark.streaming import StreamingContext 
import redis
# Set up logging 
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
#data_stream = ssc.socketTextStream("localhost", 5000) 
data_stream = ssc.socketTextStream("172.18.0.0", 5000) 
 
def send_data_to_socket(host, port, data): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s.connect((host, port)) 
        s.sendall(data.encode()) 
        print(f"Sent data: {data}") 
 
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
 
# Initialize Redis client 
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0) 
redis_client = redis.StrictRedis(host='172.18.0.1', port=6379, db=0) 
 
def process_data(rdd):  
    try:  
        data = rdd.collect()  
        for item in data:  
            item_dict = json.loads(item.replace("'", "\""))  
            if validate_data(item_dict): 
                redis_client.rpush("processed_data", json.dumps(item_dict))  
                print(f"Sent data to Redis: {item_dict}") 
    except Exception as e:  
        logging.error(f"Error processing data: {str(e)}")  

 
# Process the data stream 
data_stream.foreachRDD(process_data) 
 
if __name__ == '__main__': 
    try: 
        ssc.start() 
        ssc.awaitTermination() 
    except Exception as e: 
        logging.critical(f"Fatal error: {e}")
