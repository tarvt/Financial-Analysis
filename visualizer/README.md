# Run

**prometheus**

```
# docker
docker pull prom/prometheus
docker tag prom/prometheus localhost:5001/prometheus && sudo docker push localhost:5001/prometheus

# kubernetes
kubectl apply -f prometheus
kubectl port-forward <pod_name> 9090:9090 --namespace=prometheus

# verify
kubectl get pods
curl 127.0.0.1:9090

# stop and remove
kubectl delete -f prometheus
```

**grafana**

```
# docker
docker pull grafana/grafana
docker tag grafana/grafana localhost:5001/grafana && sudo docker push localhost:5001/grafana

# kuberentes
kubectl apply -f grafana
kubectl port-forward <pod_name> 3000:3000
```

Get prometheus ip using `kubectl get svc` and use it for adding datasource in grafana.
Grafana's default authentication is admin:admin. It asks for new password. Set it to 123456.
