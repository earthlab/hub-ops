Setting up a new cluster
========================

These are notes from winter 2021 about setting up a new cluster from
scratch.

Short version
-------------

Resources
---------

* `setup pages <https://earthlab-hub-ops.readthedocs.io/en/latest/setup/google-cloud-setup.html>`_ for this project
* `z2jh documentation <https://zero-to-jupyterhub.readthedocs.io/en/latest/index.html>`_

Assumptions
-----------

* have a gcloud project :code:`ea-jupyter` and the gcloud command line tools set up
* have kubectl and helm 3 installed

Long version
------------

What follows are "this is what I did, including mistakes that needed to be fixed" rather than "follow these steps exactly as a tutorial".

Creating a new kubernetes cluster
#################################

Create a new cluster called :code:`jhub2` in the ea-jupyter project::

  gcloud container clusters create jhub2 \
      --num-nodes=1 --machine-type=n1-standard-2 \
      --zone=us-central1-b --image-type=cos_containerd \
      --enable-autoscaling --max-nodes=3 --min-nodes=1

Reference https://cloud.google.com/sdk/gcloud/reference/container/clusters/create

Changes from cluster creation in existing docs are:

* use the default version of kubernetes rather than specifying a version. You can see the default version of kubernetes using :code:`gcloud container get-server-config`. At this moment, the defaultVersion on the RELEASE channel is 1.17.13-gke.2600.

* use the containerd image type rather than the default cos type because the latter is being deprecated, see https://cloud.google.com/kubernetes-engine/docs/concepts/using-containerd

Output from cluster creation includes the following warnings::

  WARNING: Starting in January 2021, clusters will use the Regular release channel by default when `--cluster-version`, `--release-channel`, `--no-enable-autoupgrade`, and `--no-enable-autorepair` flags are not specified.
  WARNING: Currently VPC-native is not the default mode during cluster creation. In the future, this will become the default mode and can be disabled using `--no-enable-ip-alias` flag. Use `--[no-]enable-ip-alias` flag to suppress this warning.
  WARNING: Starting with version 1.18, clusters will have shielded GKE nodes by default.
  WARNING: Your Pod address range (`--cluster-ipv4-cidr`) can accommodate at most 1008 node(s).

and this status::

  NAME   LOCATION       MASTER_VERSION    MASTER_IP       MACHINE_TYPE   NODE_VERSION      NUM_NODES  STATUS
  jhub2  us-central1-b  1.16.15-gke.4901  35.184.210.231  n1-standard-2  1.16.15-gke.4901  1          RUNNING

The create a static ip::

  gcloud compute addresses create jhub2-ip --region us-central1

List the ip addresses for the cluster(s)::

  $ gcloud compute addresses list
  NAME      ADDRESS/RANGE   TYPE      PURPOSE  NETWORK  REGION       SUBNET  STATUS
  jhub-ip   35.226.96.84    EXTERNAL                    us-central1          IN_USE
  jhub2-ip  35.225.148.166  EXTERNAL                    us-central1          RESERVED

This is a single node cluster with the n1-standard-2 node type. In the current jhub cluster, the core-pool is a custom node type and there is also a node pool. There does not seem to be documentation about setting this up in our notes, but the z2jh has `notes on setting up a node-pool on GKE <https://zero-to-jupyterhub.readthedocs.io/en/latest/kubernetes/google/step-zero-gcp.html>`_ (see step 7).

Create the user user pool (using n1-standard-8 nodes with autoscaling maximum at 5 nodes)::

  gcloud beta container node-pools create user-pool \
  --machine-type n1-standard-8 \
  --num-nodes 0 \
  --enable-autoscaling \
  --min-nodes 0 \
  --max-nodes 5 \
  --node-labels hub.jupyter.org/node-purpose=user \
  --node-taints hub.jupyter.org_dedicated=user:NoSchedule \
  --zone us-central1-b \
  --cluster jhub2

Forgot to set the image type to :code:`cos_containerd` to match the core-pool, so I changed that using the web console UI.

Install JupyterHub
##################

Following https://zero-to-jupyterhub.readthedocs.io/en/latest/jupyterhub/installation.html::

  $ helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
  $ helm repo update

Add the secret token from :code:`secrets/staginghub.yaml` to config.yaml as specified in the z2jh docs (will set up the decryption of secrets later and before committing this file!) and then install the helm chart::

  helm upgrade staginghub jupyterhub/jupyterhub --install \
  --cleanup-on-fail --namespace staginghub --create-namespace \
  --version 0.10.6 --values config.yaml

Set up docker image and gitpuller
#################################

See https://zero-to-jupyterhub.readthedocs.io/en/latest/jupyterhub/customizing/user-environment.html, added the following to config.yaml::

  singleuser:
    image:
      name: earthlabhubops/ea-k8s-user-staginghub
      tag: 9d034c2
    lifecycleHooks:
      postStart:
        exec:
          command: ["gitpuller", "https://github.com/earthlab-education/ea-bootcamp-fall-2020", "master", "ea-bootcamp-shared"]

Remove the token from config.yaml and provide it on the command line when we upgrade (also add a timeout to allow for downloading the image)::

  helm upgrade --cleanup-on-fail staginghub jupyterhub/jupyterhub --namespace staginghub --version 0.10.6 --timeout 600s --debug -f config.yaml -f ../../secrets/staginghub.yaml

Ingress and https
#################

Ingress
~~~~~~~

In order to have multiple hubs at the same URL (e.g. hub.earthdatascience.org/hub1, hub.earthdatascience.org/hub2, etc) we need to set up an ingress controller. As recommended by the z2jh team, we use kubernetes/ingress-nginx. Following the ingress-nginx `Helm installation instructions <https://kubernetes.github.io/ingress-nginx/deploy/#using-helm>`_::

  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  helm repo update

  kubectl create namespace ingress-nginx
  helm install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx

The output includes the following info::

  An example Ingress that makes use of the controller:

    apiVersion: networking.k8s.io/v1beta1
    kind: Ingress
    metadata:
      annotations:
        kubernetes.io/ingress.class: nginx
      name: example
      namespace: foo
    spec:
      rules:
        - host: www.example.com
          http:
            paths:
              - backend:
                  serviceName: exampleService
                  servicePort: 80
                path: /
      # This section is only required if TLS is to be enabled for the Ingress
      tls:
          - hosts:
              - www.example.com
            secretName: example-tls

  If TLS is enabled for the Ingress, a Secret containing the certificate and key must also be provided:

    apiVersion: v1
    kind: Secret
    metadata:
      name: example-tls
      namespace: foo
    data:
      tls.crt: <base64 encoded cert>
      tls.key: <base64 encoded key>
    type: kubernetes.io/tls

Cert-manager
~~~~~~~~~~~~

Now we need a TLS certificate manager for https. Here, we deviate from the z2jh documentation and use cert-manager rather than the (deprecated) kube-lego. Following the `cert-manager installation guide <https://cert-manager.io/docs/installation/kubernetes/>`_, specifically the parts about installing with heml::

  kubectl create namespace cert-manager
  helm repo add jetstack https://charts.jetstack.io
  helm repo update

Then install the custom resource definitions (CRDs)::

  kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.1.0/cert-manager.crds.yaml

And install the helm chart::

  helm install cert-manager jetstack/cert-manager --namespace cert-manager  --version v1.1.0

Check the installation::

  kubectl get pods --namespace cert-manager

Now you need to install a clusterIssuer resource (this is very poorly documented in the cert-manager docs, presumably because they assume their users know more about k8s than I do).

Create a :code:`cluster-issuer.yaml` file based on the `ACME template <https://cert-manager.io/docs/configuration/acme/#configuration>`_, using::

  name=letsencrypt-prod
  email=Leah.Wasser@colorado.edu
  url=https://acme-v02.api.letsencrypt.org/directory

And create (and check) the clusterissuer::

  kubectl create -f cluster-issuer.yaml
  kubectl describe clusterissuer letsencrypt-prod

Updating values.yaml
~~~~~~~~~~~~~~~~~~~~

Add the following setup to you values.yaml file::

  proxy:
    service:
      type: ClusterIP

  hub:
    baseUrl: /staginghub/

  ingress:
    enabled: true
    hosts:
      - hub.earthdatascience.org
    annotations:
      kubernetes.io/ingress.class: nginx
      cert-manager.io/cluster-issuer: "letsencrypt-prod"
    tls:
      - secretName: cert-manager-tls
        hosts:
          - hub.earthdatascience.org

Then upgrade helm::

  helm upgrade --cleanup-on-fail staginghub jupyterhub/jupyterhub --namespace staginghub --version 0.10.6 --timeout 600s --debug -f config.yaml -f ../../secrets/staginghub.yaml

I had to delete the proxy-public service that got created before switching over to manual ingress setup::

  kubectl delete service proxy-public -n staginghub

and upgrade helm.

Automatic updating
##################
 
In the GCloud console UI, find the jhub2 GKE cluster, and the release channel option. Change the setting from :code:`Static version` to :code:`Release channel` and choose the Stable channel.
