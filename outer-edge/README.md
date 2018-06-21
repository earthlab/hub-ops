# Routing to individual hubs

🚧 setup, chart and notes are all still under ehavy construction 🚧
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

Currently bundling these two together into a meta chart does not work. It seems
the creation of RBAC roles is borked and as a result kube-lego can't access what
it needs about the ingresses.

Installed nginx-ingress v0.20.1 via
```
helm install stable/nginx-ingress --name ingress --namespace router --set rbac.create=true --set controller.service.loadBalancerIP=35.226.96.84
```

The IP address is the current static IP for this deployment. Check `setup.md`
in the top level directory for how to obtain a new IP or list all IP addresses
currently in use.

and installed kube-lego v0.4.2 via
```
helm install --name lego --namespace router stable/kube-lego --set rbac.create=true --set config.LEGO_EMAIL=Leah.Wasser@colorado.edu --set config.LEGO_URL=https://acme-v01.api.letsencrypt.org/directory
```

Set IP address by hand, unsure why I needed this:
```
kubectl patch svc --namespace router ingress-nginx-ingress-controller -p '{"spec": {"loadBalancerIP": "35.226.96.84"}}'
```
