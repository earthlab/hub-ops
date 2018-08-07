# Assorted tools

A collection of various tools that have no other place to go.

## Forced cluster scaling

To force the cluster to scale up use `scale-cluster.yaml`. It
will schedule two big pods that will lead to two new nodes being
provisioned. To start the process run `kubectl create -f scale-cluster.yaml`
from this directory. These pods will request 5 units of CPU which
is more than half the amount of CPU each node provides.

Use `kubectl get pods --namespace bootcamp-hub` to check your additional pods
have been scheduled and are running. These pods request a lot of CPU in order
to trigger the scaling up, but they don't do anything with it, and while they
have requested it no one else can use it either.

The next step is to run `kubectl create -f pin-cluster.yaml` which will start
the same number of pods requesting nearly no CPU. Once these are up and running
we can remove the big pods again as the autoscaler will not remove a virtual
machine that has pods running on it.

To remove the big pods: `kubectl delete deployment cluster-scale-deployment --namespace=bootcamp-hub`. You can safely leave the small pods running until
after the class/workshop/event is over as they consume nearly no resources.
After the envet is over you want to delete them again to allow the cluster to
shrink again, use: `kubectl delete deployment cluster-pin-deployment --namespace=bootcamp-hub`
to do so. After about 10-15minutes nodes that are not needed anymore should
start being removed.
