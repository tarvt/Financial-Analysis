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
sudo docker build -t localhost:5001/exporter . && sudo docker push localhost:5001/exporter

# run
sudo docker run -p 9877:9877 localhost:5001/exporter
```

**kubernetes**

```
# run
kubectl apply -f kubernetes.yaml

# test
kubectl create deployment exporter --image=localhost:5001/exporter
kubectl port-forward <pod_name> 9877:9877

# verify
kubectl get pods
curl 127.0.0.1:9877
kubectl get svc
curl 172.18.0.x:9877

# stop 
kubectl delete -f kubernetes.yaml
kubectl delete deployment exporter
```
