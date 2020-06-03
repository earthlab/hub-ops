.. _troubleshooting:

Troubleshooting Hub Deployments
===============================

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

GCloud authentication
~~~~~~~~~~~~~~~~~~~~~

If you get permission errors using ``kubectl``, check your authentication::

  gcloud auth list

If the active account is ``travis-deployer``, you need to switch back to your personal 
account (which will be the one with your gmail account). This can happen if you run 
the ``deploy.py`` script locally, which is designed to be run by Travis. Somehow, 
this authentication gets saved to your kubectl config / cache. To fix:

* remove (or rename) the ``~/.kube`` directory in your local home folder
* re-authenticate using ``gcloud container clusters get-credentials jhub --region us-central1-b``

Helpful CLI commands
~~~~~~~~~~~~~~~~~~~~

You can view and edit components of your cluster from the command line using a combination of commands from Google Cloud SDK, Kubernetes, and Helm.

GCloud commands::

  $ gcloud containers cluster list  # list your clusters (probably only one; jhub)

  $ gcloud container clusters describe jhub  # show details about the cluster ``jhub``

  $ gcloud auth list # list all gcloud authentications; highlights active authentication

**Kubernetes commands**

You can view and edit your kubernetes cluster using `kubectl`. There is a great cheat sheet in the official docs: https://kubernetes.io/docs/reference/kubectl/cheatsheet/

Short list of kubectl commands::

  $ kubectl get namespace  # list of namespaces

  $ kubectl get pods -n <namespace>  # list all pods in a namespace

  $ kubectl logs -n <namespace> <podname> # get logs for a single pod

  $ kubectl get events -n <namespace> --sort-by='{.lastTimestamp}'  # get events for a pod

  $ kubectl get pvc -n <namespace>  # get list of PersistentVolumeClaims
