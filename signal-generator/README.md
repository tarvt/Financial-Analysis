# Signal Generator 

Input:  processor 5005 (service)
output: self      -

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
sudo docker build -t localhost:5001/signal-generator . && sudo docker push localhost:5001/signal-generator

# run
sudo docker run -p 5005:5005 localhost:5001/signal-generator
```

**kubernetes**

```
# run
kubectl apply -f kubernetes.yaml

# test
kubectl create deployment signal-generator --image=localhost:5001/signal-generator

# verify
kubectl get pods

# stop 
kubectl delete -f kubernetes.yaml
kubectl delete deployment signal-generator
```
