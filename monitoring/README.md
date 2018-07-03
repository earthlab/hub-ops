# Monitoring for the hubs

Deploy from the top level directory with:
```
$ (cd monitoring && helm dep up)
$ helm upgrade --install --namespace monitoring monitoring monitoring --version=v0.1.0 -f secrets/monitoring.yaml
```
