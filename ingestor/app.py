import logging
import requests
import time
import datetime  # Import the datetime module

logging.basicConfig(filename='ingestor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def continuous_reader():
    while True:
        try:
            response = requests.get('http://172.18.0.0:5000')
            response.raise_for_status()  # Raise an exception if the request fails

            received_data = response.json()  # Assuming JSON response
            logging.info(f"Received data: {received_data}")

        except Exception as e:
            logging.error(f"Error: {str(e)}")

        time.sleep(1)  # Adjust the polling interval as needed

if __name__ == '__main__':
    continuous_reader()

