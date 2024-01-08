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
