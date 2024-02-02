kubectl version:
Client Version: v1.28.4
Server Version: v1.27.3

**install**

```
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

**interact with cluster**

```
# start cluster
bash kind.sh

# verify cluster is up
sudo docker ps

# stop cluster
kind delete cluster
```

**helm**

```
wget https://get.helm.sh/helm-v3.13.3-linux-arm64.tar.gz
tar -zxvf  helm-v3.13.3-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
```
helm version
Version:"v3.13.3"


**metallb**

```
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb

# find docker network ip
docker network inspect -f '{{.IPAM.Config}}' kind

# set docker network ip as the address pool
kubectl apply -f ipaddresspool.yaml

# verify everything is fine
kubectl get services
```
