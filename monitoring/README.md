# Monitoring for the hubs

These files define the `monitoring` hub that underlies https://grafana.hub.earthdatascience.org.

Deployment of the monitoring hub happens automatically through travis and the deploy.py script. To deploy manually: 

```
$ (cd monitoring && helm dep up)
$ helm upgrade --install --namespace monitoring monitoring monitoring --version=v0.1.0 -f secrets/monitoring.yaml
```
