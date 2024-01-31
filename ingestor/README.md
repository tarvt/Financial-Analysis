# Run

**python**

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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
# test deployment
kubectl create deployment ingestor-app-server --image=localhost:5001/ingestor-app:latest
kubectl port-forward <pod_name> 5002:5002

# verify
kubectl get pods

# stop and remove deployment
kubectl delete pod <pod_name>
kubectl delete deployment ingestor-app-server

# run all manifests
# BEWARE: YOU MUST HAVE INSTALLED HELM AND SETUP METALLB FIRST!
kubectl apply -f kubernetes/
# wait until metallb speakers change their states into running

# verify
curl 172.18.0.0:5002

# delete all manifests
kubectl delete -f kubernetes/
```

