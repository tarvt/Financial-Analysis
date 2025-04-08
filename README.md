# Real-Time Financial Analysis & Trading System
The project aims to develop a comprehensive Real-Time Financial Analysis & Trading System that enables users to analyze financial data, generate trading signals, and receive instant notifications. 
Written by: Taravat Monsef, Hatam Abolghasemi


## Tools Used
- **PySpark**: For real-time data processing and calculation of trading indicators (Moving Average, Exponential Moving Average, and Relative Strength Index).
- **Redis**: High-performance, in-memory data store that enhances data processing speed and reliability, facilitates caching, and ensures seamless data transfer.
- **Prometheus**: Monitoring and visualization tool that collects and stores metrics related to system performance, resource utilization, and user interactions.



### Key Components

#### 1. Generator
##### Component Overview
- **Data Generation Functions**:
  - `generate_data()`: Generates financial data such as opening price, closing price, volume, and timestamp for randomly selected stock symbols.
  - `generate_additional_data()`: Produces additional financial data types (e.g., order book information, news sentiment).
- **Data Sending Function**:
  - `generate_and_send_data()`: Continuously generates data and sends it over a TCP connection with random sleep intervals.
- **Socket Server Function**:
  - `socket_server()`: Sets up a TCP socket server to start sending generated data and logs server connection events.

##### How Data is Sent
Generated financial data is formatted as a JSON string and sent over the TCP connection established with the client at random intervals.
#### 2. Ingestor
##### Component Overview
- **Logging Setup**: Configures two loggers for received and validated data.
- **Spark Streaming Setup**: Initializes SparkContext and StreamingContext to process data with a 1-second interval.
- **Data Stream Configuration**: Listens for incoming data on specific ports.
- **Data Validation Function**: Ensures incoming data meets predefined criteria before storage.
- **Sending Data to Redis**: Validated data is pushed to a Redis list named "processed_data" for analysis.


##### How Data is Handled
Incoming data is processed in batches, validated, and stored in Redis for further processing.
#### 3. Processor
##### Component Overview
- **Spark and Streaming Context Initialization**: Initializes a SparkSession for data processing.
- **Redis Client Setup**: Connects to Redis to fetch processed data.
- **Data Processing Functions**: Functions for calculating moving averages and other indicators.
- **Data Streaming and Processing**: Continuously updates Pandas Series for various data types and sends processed data.
- **Data Sending and Exception Handling**: Formulates processed data for sending to an endpoint.

##### How Data is Handled
Data is fetched from Redis, processed for indicators, and prepared for further analysis or visualization.


## Exporter
- **Prometheus Client Import**: Imports metrics functions necessary for monitoring.
- **Metric Creation**: Creates Gauge metrics for MA, EMA, and RSI values.
- **Metric Updates**: Regularly updates metrics with the latest calculated values.
- **Starting the Exporter**: Starts an HTTP server to expose metrics for Prometheus scraping.


## Kubernetes Manifests
- **Deployment**: Defines how to create and manage instances of the "generator" service with specific configurations.
- **Service**: Sets up an endpoint for accessing the "generator" service, allowing external access.


### Reusable Pattern
Other services (ingestor, processor) follow similar patterns in their deployment, enhancing scalability and maintainability.


## Dockerfiles
### Key Instructions
1. **Base Image**: Starts from a lightweight Python 3.11 base image.
2. **Working Directory**: Sets `/app` as the working directory.
3. **Copying Requirements**: Installs dependencies specified in `requirements.txt`.
4. **Copying Application Code**: Copies the main application code file.
5. **Default Command**: Specifies the default command to run the application.
6. **Exposing Port**: Indicates that the container listens on port 5000.


### Reusable Pattern
Each service has its Dockerfile pattern, facilitating maintainability and isolation.

## Challenge
- **Communication Breakdown**: Encountered issues with the communication between Generator and Ingestor components when Dockerized, requiring further investigation.





 
