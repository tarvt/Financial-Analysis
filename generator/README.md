# Run

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
sudo docker build -t localhost:5001/generator . && sudo docker push localhost:5001/generator

# run
sudo docker run -p 5000:5000 localhost:5001/generator
```

**kubernetes**

```
# run
kubectl apply -f kubernetes.yaml

# test
kubectl create deployment generator --image=localhost:5001/generator
kubectl port-forward <pod_name> 5000:5000

# verify
kubectl get pods
curl 127.0.0.1:5000
kubectl get svc
curl 172.18.0.x:5000

# stop 
kubectl delete -f kubernetes.yaml
kubectl delete deployment generator
```

