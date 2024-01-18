# Run

**build**
```
source venv/bin/activate
pip install -r requirements.txt
```

**run**

```
# python
cd project
python manage.py runserver

# uwsgi
cd project
uwsgi --ini uwsgi.ini 
```


**django admin panel**

```
user: hatam
email: hatamabolghasemi97@yahoo.com
pass: Anathema
```

**docker**

```
# build and push to kind registry
sudo docker build -t generator-app . && sudo docker tag generator-app localhost:5001/generator-app && sudo docker push localhost:5001/generator-app

# run
sudo docker run -p 5000:5000 localhost:5001/generator-app:latest
```

**helm**

```
wget https://get.helm.sh/helm-v3.13.3-linux-arm64.tar.gz
tar -zxvf  helm-v3.13.3-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
```

**metallb**

```
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb
```

**kubernetes**

```
# test deployment
kubectl create deployment generator-app-server --image=localhost:5001/generator-app:latest
kubectl port-forward <pod_name> 5000:5000

# verify
kubectl get pods

# stop and remove deployment
kubectl delete pod <pod_name>
kubectl delete deployment generator-app-server

# run all manifests
# BEWARE: YOU MUST HAVE INSTALLED HELM AND SETUP METALLB FIRST!
kubectl apply -f kubernetes/
# wait until metallb speakers change their states into runngin

# verify
curl 172.18.0.0:5000

# delete all manifests
kubectl delete -f kubernetes/
```


Don't forget that you've hardcoded loadbalancer's ip into setting.py as allowed host. find a better solution later. it's not clean.
