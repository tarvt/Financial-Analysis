import socket 
import logging 
import time 
import random 
import numpy as np 
from threading import Thread 
 
# Configuration for the socket server 
TCP_IP = '127.0.0.1' 
# TCP_IP = '0.0.0.0' 
TCP_PORT = 5000 
BUFFER_SIZE = 1024 



# Initialize the logger 
logging.basicConfig(filename='generator.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') 
 
stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"] 


def generate_data():
    global data
    stock_symbol = random.choice(stocks)
    prev_price = 1000 
    dt = 1 
    mu = 0.0002 
    sigma = 0.01 

    price_change = np.exp((mu - 0.5 * sigma**2) * dt +
              sigma * np.sqrt(dt) * np.random.normal())
    opening_price = max(0, prev_price * price_change)
    closing_price = max(0, opening_price +
              round(random.normalvariate(0, 10), 2))
    high = max(opening_price, closing_price) + \
              round(abs(random.normalvariate(0, 5)), 2)
    low = min(opening_price, closing_price) - \
              round(abs(random.normalvariate(0, 5)), 2)
    volume = max(0, int(np.random.poisson(5000) *
              (1 + 0.1 * np.random.normal())))

    data = {
        "stock_symbol": stock_symbol,
        "opening_price": opening_price,
        "closing_price": closing_price,
        "high": high,
        "low": low,
        "volume": volume,
        "timestamp": time.time()
    }
    return data


def generate_additional_data():
    stock_symbol = random.choice(stocks)
    timestamp = time.time()
    data_types = ['order_book', 'news_sentiment',
           'market_data', 'economic_indicator']
    data_type = random.choice(data_types)

    if data_type == 'order_book':
        data = {
            "data_type": "order_book",
            "timestamp": timestamp,
            "stock_symbol": stock_symbol,
            "order_type": random.choice(['buy', 'sell']),
            "price": random.uniform(100, 1000),
            "quantity": random.randint(1, 100)
        }
    elif data_type == 'news_sentiment':
        data = {
            "data_type": "news_sentiment",
            "timestamp": timestamp,
            "stock_symbol": stock_symbol,
            "sentiment_score": random.uniform(-1, 1),
            "sentiment_magnitude": random.uniform(0, 1)
        }
    elif data_type == 'market_data':
        data = {
            "data_type": "market_data",
            "timestamp": timestamp,
            "stock_symbol": stock_symbol,
            "market_cap": random.uniform(1e9, 1e12),
            "pe_ratio": random.uniform(5, 30)
        }
    elif data_type == 'economic_indicator':
        data = {
            "data_type": "economic_indicator",
            "timestamp": timestamp,
            "indicator_name": "GDP Growth Rate",
            "value": random.uniform(-5, 5)
        }
    logging.info(f"Generated Data: {data}")
    return data


def generate_and_send_data(conn): 
    try: 
        while True: 
            data = generate_additional_data() 
            message = f"{data}\n" 
            conn.send(message.encode()) 
            time.sleep(random.uniform(1, 5)) 
            print(f"data sent : {data}")
    except Exception as e: 
        logging.critical(f"Error sending data: {e}") 
 
def socket_server(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((TCP_IP, TCP_PORT)) 
    s.listen(1) 
     
    logging.info(f"Listening on port {TCP_PORT}...") 
 
    conn, addr = s.accept() 
    logging.info(f"Connection address: {addr}") 
 
    generate_and_send_data(conn) 
    conn.close() 
 
if __name__ == "__main__": 
    try: 
        server_thread = Thread(target=socket_server) 
        server_thread.start() 
    except Exception as e: 
        logging.critical(f"Fatal error: {e}")
