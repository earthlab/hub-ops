.. _troubleshooting:

Troubleshooting Hub Deployments
===============================

TODO: NOTE: this may be it's own section in the future but starting it here for
now.

If a Deployment Hangs
~~~~~~~~~~~~~~~~~~~~~~
Failed deployments can be frustrating because there is often not a useful error
when running via CI or locally. When a deployment fails via a timeout, you
can explore the most recent events associated with the namespace (namespace
referring to the hub name for example ``edsc-hub``). This will provide you
with more information about why the most recent hub deployment failed for a
specific namespace.

For more discussion see: https://github.com/helm/charts/issues/11904#issuecomment-611368714

The Earth Lab Hub deployment has multiple hubs that are deployed from a single
google cloud project. To begin you may want to view a list of available
namespaces (hubs) in your google cloud project. To do that use::

  kubectl get namespace

Then select the namespace that you wish to get more information for and run the
following::

  kubectl -n <namespace> get events --sort-by='{.lastTimestamp}'

Sometimes, if the deployment fails, you can try uninstalling and re-installing
the helm chart. For example, if you list the helm charts and one has status
failed::

  $  hub-ops git:(staging) ✗ helm list --all --all-namespaces
  NAME         	NAMESPACE    	REVISION	UPDATED                               	STATUS  	CHART               	APP VERSION
  cert-manager 	cert-manager 	1       	2021-01-11 10:19:55.227696 -0500 EST  	deployed	cert-manager-v1.1.0 	v1.1.0
  ingress-nginx	ingress-nginx	1       	2021-01-11 10:53:04.954353 -0500 EST  	deployed	ingress-nginx-3.19.0	0.43.0
  staginghub   	staginghub   	3       	2021-01-13 16:35:20.01524069 +0000 UTC	failed  	jupyterhub-0.10.6   	1.2.2

  $ helm uninstall staginghub -n staginghub

Then, re-run deployment, either locally or by re-running the Action.

Google Cloud Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you get permission errors using ``kubectl``, check your authentication::

  gcloud auth list

If the active account is ``travis-deployer``, you need to switch back to your personal
account (which will be the one with your gmail account). This can happen if you run
the ``deploy.py`` script locally, which is designed to be run by Travis. Somehow,
this authentication gets saved to your kubectl config / cache. To fix:

* remove (or rename) the ``~/.kube`` directory in your local home folder
* re-authenticate using::

   gcloud container clusters get-credentials jhub --region us-central1-b

Helpful CLI commands
~~~~~~~~~~~~~~~~~~~~

You can view and edit components of your cluster from the command line using a combination of commands from Google Cloud SDK, Kubernetes, and Helm.

**GCloud commands**

List your clusters (probably only one, `jhub`)::

  $ gcloud containers cluster list

Show details about cluster jhub::

  $ gcloud container clusters describe jhub

List all gcloud authentications; highlights active authentication::

  $ gcloud auth list

**Kubernetes commands**

You can view and edit your kubernetes cluster using `kubectl`. There is a great cheat sheet in the official docs: https://kubernetes.io/docs/reference/kubectl/cheatsheet/ but here are some common ones.

List namespaces::

  $ kubectl get namespace

List all pods in a namespace::

  $ kubectl get pods -n <namespace>

Get logs for a single pod::

  $ kubectl logs -n <namespace> <podname>

Get recent events for a pod::

  $ kubectl get events -n <namespace> --sort-by='{.lastTimestamp}'

Get list of PersistentVolumeClaims::

  $ kubectl get pvc -n <namespace>
