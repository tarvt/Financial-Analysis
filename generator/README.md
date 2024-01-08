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
```
