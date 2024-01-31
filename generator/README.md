# Run

**python**
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**docker**

```
# build and push to kind registry
sudo docker build -t generator-app . && sudo docker tag generator-app localhost:5001/generator-app && sudo docker push localhost:5001/generator-app

# run
sudo docker run -p 5000:5000 localhost:5001/generator-app:latest
```

**kubernetes**

```
# test deployment
kubectl create deployment generator-app-server --image=localhost:5001/generator-app:latest
kubectl port-forward <pod_name> 5000:5000

# verify
kubectl get pods
curl 127.0.0.1:5000

# stop and remove deployment
kubectl delete pod <pod_name>
kubectl delete deployment generator-app-server

# run all manifests
# BEWARE: YOU MUST HAVE INSTALLED HELM AND SETUP METALLB FIRST!
kubectl apply -f kubernetes/
# wait until metallb speakers change their states into running

# verify
curl <network>:<app_port>
curl 172.18.0.0:5000

# delete all manifests
kubectl delete -f kubernetes/
```

