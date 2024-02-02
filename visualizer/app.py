"""Application exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge, Enum
import requests

class AppMetrics:
  """
  Representation of Prometheus metrics and loop to fetch and transform
  application metrics into Prometheus metrics.
  """

  def __init__(self, app_port=5005, polling_interval_seconds=5):
    self.app_port = app_port
    self.polling_interval_seconds = polling_interval_seconds

    # Prometheus metrics to collect
    self.data_type = Gauge("app_data_type", "Data type")
    self.MA = Gauge("app_MA", "MA")
    self.EMA = Gauge("app_EMA", "EMA")
    self.RSI = Gauge("app_RSI", "RSI")

  def run_metrics_loop(self):
    """Metrics fetching loop"""

    while True:
      self.fetch()
      time.sleep(self.polling_interval_seconds)

  def fetch(self):
    """
    Get metrics from application and refresh Prometheus metrics with
    new values.
    """

    # Fetch raw status data from the application
    # resp = requests.get(url=f"http://localhost:{self.app_port}/")
    resp = requests.get(url=f"http://172.18.0.4:{self.app_port}/")

    # Update Prometheus metrics with application metrics
    self.data_type.set(resp["data_type"])
    self.MA.set(resp["MA"])
    self.EMA.set(resp["EMA"])
    self.RSI.set(resp["RSI"])

def main():
  """Main entry point"""

  polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "5"))
  app_port = int(os.getenv("APP_PORT", "5005"))
  exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

  app_metrics = AppMetrics(
    app_port=app_port,
    polling_interval_seconds=polling_interval_seconds
  )
  start_http_server(exporter_port)
  app_metrics.run_metrics_loop()

if __name__ == "__main__":
  main()
