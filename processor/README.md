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

**python**
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Don't forget to `deactivate` when your work is done.
```

**docker**

```
# build and push to kind registry
sudo docker build -t localhost:5001/processor . && sudo docker push localhost:5001/processor

# run
sudo docker run -p 5005:5005 localhost:5001/processor
```

**kubernetes**

```
# run
kubectl apply -f kubernetes.yaml

# test
kubectl create deployment processor --image=localhost:5001/processor
kubectl port-forward <pod_name> 5005:5005

# verify
kubectl get pods
curl 127.0.0.1:5005
kubectl get svc
curl 172.18.0.x:5005

# stop 
kubectl delete -f kubernetes.yaml
kubectl delete deployment processor
```
