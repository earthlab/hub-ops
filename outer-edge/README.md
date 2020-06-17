# Routing to individual hubs

🚧 setup, chart and notes are all still under heavy construction 🚧
🚧 The chart doesn't work, check the individual commands in the developer notes section 🚧

This chart is responsible for the nginx-ingress and HTTPs certificates. We use
it to redirect to the individual hubs which have their own charts.

First time install command:
```
helm install outer-edge --name router --namespace router --version=v0.1.0 --set rbac.create=true
```

Deploy changes:
```
helm upgrade --install --namespace router router outer-edge --version=v0.1.0
```

## Developer notes

### Migrating from kube-lego to cert-manager

Following [cert-manager migration guide](https://cert-manager.io/docs/tutorials/acme/migrating-from-kube-lego/), noting that cert-manager installed in `cert-manager` namespace as per the installation docs, not in `kube-system` as described in the migration guide. 

```
$ kubectl scale deployment lego-kube-lego -n router --replicas=0
$ kubectl create namespace cert-manager
$ helm repo add jetstack https://charts.jetstack.io
$ helm repo update
$ kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.15.1/cert-manager-legacy.crds.yaml
$ helm install --name cert-manager --namespace cert-manager --version v0.15.1 jetstack/cert-manager
$ kubectl get pods --namespace cert-manager
$ kubectl get secret kube-lego-account -o yaml -n router --export > kube-lego-account.yaml
```

Modify the `metadata.name` field in `kube-lego-account.yaml` to
`letsencrypt-private-key`.

```
$ kubectl create -f kube-lego-account.yaml -n cert-manager
```
Create the `cluster-issuer.yaml` file as per the docs, using
name=letsencrypt-prod
email=Leah.Wasser@colorado.edu
url=https://acme-v02.api.letsencrypt.org/directory :
```
$ kubectl create -f cluster-issuer.yaml
$ kubectl describe clusterissuer letsencrypt-prod
$ helm upgrade cert-manager jetstack/cert-manager --namespace cert-manager --set ingressShim.defaultIssuerName=letsencrypt-prod --set ingressShim.defaultIssuerKind=ClusterIssuer
$ kubectl get certificates --all-namespaces  

```

### Older notes

Currently bundling these two together into a meta chart does not work. It seems
the creation of RBAC roles is borked and as a result kube-lego can't access what
it needs about the ingresses.

Installed nginx-ingress v0.20.1 via
```
helm install stable/nginx-ingress --name ingress --namespace router --set rbac.create=true --set controller.service.loadBalancerIP=35.226.96.84
```
To upgrade the deployment after config changes:
```
helm upgrade --namespace router ingress stable/nginx-ingress -f outer-edge/values.yaml
```

The IP address is the current static IP for this deployment. Check `setup.md`
in the top level directory for how to obtain a new IP or list all IP addresses
currently in use.

and installed kube-lego v0.4.2 via
```
helm install --name lego --namespace router stable/kube-lego --set rbac.create=true --set config.LEGO_EMAIL=Leah.Wasser@colorado.edu --set config.LEGO_URL=https://acme-v01.api.letsencrypt.org/directory
```

To update or change the configuration of kube-lego use:
```
helm upgrade --namespace router lego stable/kube-lego -f outer-edge/values.yaml --set rbac.create=true
```

Set IP address by hand, unsure why I needed this:
```
kubectl patch svc --namespace router ingress-nginx-ingress-controller -p '{"spec": {"loadBalancerIP": "35.226.96.84"}}'
```
