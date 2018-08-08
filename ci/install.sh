#!/bin/bash
set -ex

echo $PATH

# install nsenter if missing (needed by kube on trusty)
if ! which nsenter; then
  curl -L https://github.com/minrk/git-crypt-bin/releases/download/trusty/nsenter > nsenter
  echo "5652bda3fbea6078896705130286b491b6b1885d7b13bda1dfc9bdfb08b49a2e  nsenter" | shasum -a 256 -c -
  chmod +x nsenter
  sudo mv nsenter /usr/local/bin/
fi

# install kubectl, minikube
# based on https://blog.travis-ci.com/2017-10-26-running-kubernetes-on-travis-ci-with-minikube
echo "installing kubectl"
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.10.0/bin/linux/amd64/kubectl
chmod +x kubectl
mv kubectl $HOME/bin/
which kubectl

echo "installing minikube"
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.28.2/minikube-linux-amd64
chmod +x minikube
mv minikube $HOME/bin/

echo "starting minikube with RBAC"
sudo CHANGE_MINIKUBE_NONE_USER=true $HOME/bin/minikube start --vm-driver=none --kubernetes-version=v1.10.0 --extra-config=apiserver.Authorization.Mode=RBAC --bootstrapper=localkube
minikube update-context

echo "waiting for kubernetes"
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'
until kubectl get nodes -o jsonpath="$JSONPATH" 2>&1 | grep -q "Ready=True"; do
  sleep 1
done
kubectl get nodes

echo "installing helm"
curl -ssL https://storage.googleapis.com/kubernetes-helm/helm-v2.9.1-linux-amd64.tar.gz \
  | tar -xz -C $HOME/bin --strip-components 1 linux-amd64/helm
chmod +x $HOME/bin/helm

kubectl --namespace kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --service-account tiller


echo "waiting for tiller"
kubectl --namespace=kube-system rollout status --watch deployment/tiller-deploy
