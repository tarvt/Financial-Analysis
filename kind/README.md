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
# way 1
wget https://get.helm.sh/helm-v3.13.3-linux-arm64.tar.gz
tar -zxvf  helm-v3.13.3-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm

# way 2
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
apt update
apt install helm

# verification
helm version
```

**metallb**

```
# install
helm repo add metallb https://metallb.github.io/metallb
helm install metallb metallb/metallb

# find docker network ip
docker network inspect -f '{{.IPAM.Config}}' kind

# set docker network ip as the address pool
kubectl apply -f ipaddresspool.yaml

# verifification
kubectl get services
```

