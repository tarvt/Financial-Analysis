# Functionality 
Listens for incoming financial data on a specified port. 
Validates the incoming data based on predefined criteria. 
Streams valid data to Redis for further processing. 
# Usage 
Start the Ingestor script. Ensure it's configured to listen on the correct port for incoming data and to connect to Redis on the default port (6379). 
 
The Ingestor processes data and sends it to Redis under a specific key (e.g., processed_data).

# Run
## Setting up Redis 
Before running the Ingestor and Processor, ensure that the Redis server is installed and running. Redis acts as a broker, allowing the Ingestor to stream data to it, and the Processor to consume this data. 
 
Install Redis: Follow the instructions on the official Redis website to install Redis on your system. 
Start Redis Server: Run the Redis server. By default, Redis listens on port 6379. 

**redis**
```
systemctl restart redis-server
sudo systemctl status redis-server

docker pull redis
docker tag redis localhost:5001/redis && sudo docker push localhost:5001/redis
```

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
sudo docker build -t ingestor-app . && sudo docker tag ingestor-app localhost:5001/ingestor-app && sudo docker push localhost:5001/ingestor-app

# run
sudo docker run -p 5002:5002 localhost:5001/ingestor-app:latest
```

**kubernetes**

```
# run
kubectl apply -f kubernetes.yaml

# test
kubectl create deployment ingestor-app --image=localhost:5001/ingestor-app:latest
kubectl port-forward <pod_name> 5000:5000

# verify
kubectl get pods
curl 127.0.0.1:5002
kubectl get svc
curl 172.18.0.x:5002

# stop 
kubectl delete -f kubernetes.yaml
kubectl delete deployment ingestor-app

```
