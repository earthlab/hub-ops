.. _troubleshooting:

Troubleshooting a Failed Deployment
===================================

TODO: NOTE: this may be it's own section in the future but starting it here for
now.

If a Deployment Hangs
~~~~~~~~~~~~~~~~~~~~~~
Failed deployments can be frustrating because there is often not a useful error
when running via travis or locally. When a deployment fails via a timeout, you
can explore the most recent events associated with the namespace (namespace
referring to the hub name for example ``edsc-hub``). This will provide you
with more information about why the most recent hub deployment failed for a
specific namespace.

For more discussion see: https://github.com/helm/charts/issues/11904#issuecomment-611368714

The Earth Lab Hub deployment has multiple hubs that are deployed from a single
google cloud project. To begin you may want to view a list of available
namespaces (hubs) in your google cloud project.

``kubectl get namespace``

Then select the namespace that you wish to get more information for and run the
following:

``kubectl -n <namespace> get events --sort-by='{.lastTimestamp}'``
