from prometheus_client import start_http_server, Gauge
import requests
import time

# Create Prometheus metrics
ma_metric = Gauge('market_data_ma', 'Moving Average')
ema_metric = Gauge('market_data_ema', 'Exponential Moving Average')
rsi_metric = Gauge('market_data_rsi', 'Relative Strength Index')

def fetch_data():
    url = 'http://127.0.0.1:5005'
    response = requests.get(url)
    data = response.json()
    return data

def update_metrics():
    data = fetch_data()
    # Update Prometheus metrics
    ma_metric.set(data['MA'])
    ema_metric.set(data['EMA'])
    rsi_metric.set(data['RSI'])

if __name__ == '__main__':
    # Start the Prometheus exporter
    start_http_server(9877)
    
    # Periodically update the metrics
    while True:
        update_metrics()
        time.sleep(5)  # Update every 60 seconds
