# Processor 
## Functionality 
Listens for new data in Redis. 
Processes the data by calculating financial indicators such as Moving Average (MA), Exponential Moving Average (EMA), and Relative Strength Index (RSI). 
Sends the processed data to a specified port for further use (e.g., a trading signal service). 
## Usage 
Start the Processor script. It will continuously check Redis for new data. 
 
Upon receiving data, the Processor calculates the required financial indicators and sends the results to a designated port. 
 
## Connecting Ingestor and Processor via Redis 
The Ingestor and Processor are connected through Redis. The Ingestor pushes validated data into Redis, and the Processor, upon detecting new data in Redis, retrieves and processes it. This setup decouples the two components, allowing for more robust and scalable data processing.