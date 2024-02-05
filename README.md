# Financial-Analysis 
3 - Distributed Systems Project 

Written by: Taravat Monsef, Hatam Abolghasemi

## Scenario 
 
1. generator  
    1. generates simulated financial data from multiple sources. 
    2. modifies the generated data. 
    3. send the modified data to data-ingestor 
     
    --- 
     
2. data-ingestor  
    1. receives the simulated data from multiple sources. 
    2. validates the received data. 
    3. forwards the validated data to stream-processor 
     
    --- 
     
3. stream-processor  
    1. processes the data in real-time 
    2. analyzes the processed data 
    3. calculate the mandatory trading indicators (Moving Average, Exponential Moving Average, Relative Strength Index (RSI)) 
    4. forwards the calculated indicators and analyzed data to signal-generator 
     
    --- 
     
4. signal-generator  
    1. generates buy/sell signals based on the analyzed data 
    2. forward the generated signals to the notification-generator. 
     
    --- 
     
5. notification-generator 
    1. informs users through user-interface instantly when a trading signal is generated. 
     
    --- 
     
6. visualizer  
    1. represents processed data on a user-friendly dashboard in real-time using WebSockets. 
    2. represents signals on a user-friendly dashboard in real-time using WebSockets. 
     
    --- 
     
7. load-balancer  
    1. manages incoming traffic across multiple servers. 
     
    --- 
     
8. data-aggregator  
    1. summarizes each stock’s performance. 
     
    --- 
     
9. user-interface  
    1. allows users to interact with the system 
    2. allows users to view visualized data and detailed information 
    3. allows users to receive real-time trading signals 
    4. allows users to receive notifications 
 
    --- 
 