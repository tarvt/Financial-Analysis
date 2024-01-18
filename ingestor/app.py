import logging
import requests
import time
import datetime
from flask import Flask, request, jsonify
from threading import Thread

latest_validated_data = None

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

def validate_data(data):
    required_fields = {
        "economic_indicator": ["indicator_name", "timestamp", "value"],
        "news_sentiment": ["sentiment_magnitude", "sentiment_score", "stock_symbol", "timestamp"],
        "order_book": ["order_type", "price", "quantity", "stock_symbol", "timestamp"],
        "market_data": ["market_cap", "pe_ratio", "stock_symbol", "timestamp"]
    }
    if "data_type" not in data:
        return False

    required_fields_for_type = required_fields.get(data["data_type"])
    if not required_fields_for_type:
        return False

    for field in required_fields_for_type:
        if field not in data:
            return False
    return True

def continuous_reader():
    while True:
        try:
            input = requests.get('http://172.18.0.0:5000')
            input.raise_for_status()  
            received_data = input.json()
            received_logger.info(f"Received data: {received_data}") 
            if validate_data(received_data):
                validated_logger.info(f"Validated data: {received_data}")
                global latest_validated_data
                latest_validated_data = received_data
            else:
                logging.error(f"Corrupted data: {received_data}")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        time.sleep(1)  

@app.route('/')
def get_validated_data():
    global latest_validated_data
    return latest_validated_data

if __name__ == '__main__':
    try:
        thread = Thread(target=continuous_reader)
        thread.start()
        app.run(host='0.0.0.0', port=5002)
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
