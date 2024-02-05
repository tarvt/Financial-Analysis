redis:
- input:  ingestor 6379 (exposed)
- output: processor 6379 (exposed)
prometheus:
- input:  processor-exporter 9877 (service)
- output: grafana            9090 (exposed)
grafana:
- input:  prometheus 9090 (service)
- output: self       3000 (exposed)

**docker**

```
# pull
sudo docker pull redis
sudo docker pull prom/prometheus
sudo docker pull grafana/grafana

# tag
sudo docker tag redis localhost:5001/redis
sudo docker tag prom/prometheus localhost:5001/prometheus
sudo docker tag grafana/grafana localhost:5001/grafana
```

**kubernetes**

```
# apply all three services
kubectl apply -f ../services

# apply every service seperated
kubectl apply -f redis.yaml
kubectl apply -f prometheus.yaml
kubectl apply -f grafana.yaml
```

It's suggested to apply prometheus after deploying `processor.yaml` because you'll need to apply processor's service address in prometheus ConfigMap.
