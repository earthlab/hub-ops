Setting up ingress and HTTPS
============================

.. note::

    These instructions replace the instructions in the :code:`outer-edge` directory.

In our setup, we have multiple hubs running at one URL, e.g.::

  https://hub.earthdatascience.org/staginghub
  https://hub.earthdatascience.org/ea-hub
  https://hub.earthdatascience.org/nbgrader-hub

To do this, we need to set up an ingress controller and also manage https certificates for the site.

Ingress
-------

As recommended by the z2jh team, we use kubernetes/ingress-nginx. Following the ingress-nginx `Helm installation instructions <https://kubernetes.github.io/ingress-nginx/deploy/#using-helm>`_::

    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update

    kubectl create namespace ingress-nginx
    helm install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx

Certificates with cert-manager
------------------------------

Now we need a TLS certificate manager for https. Here, we again deviate from the z2jh documentation and use cert-manager rather than the (deprecated) kube-lego. Following the `cert-manager installation guide <https://cert-manager.io/docs/installation/kubernetes/>`_, specifically the parts about installing with heml::

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

Create a :code:`cluster-issuer.yaml` file based on the `ACME template <https://cert-manager.io/docs/configuration/acme/#configuration>`_, with the following settings::

      name=letsencrypt-prod
      email=Leah.Wasser@colorado.edu
      url=https://acme-v02.api.letsencrypt.org/directory

And create (and check) the clusterissuer::

      kubectl create -f cluster-issuer.yaml
      kubectl describe clusterissuer letsencrypt-prod

Updating config.yaml
~~~~~~~~~~~~~~~~~~~~

Add the following setup to you <hubname>.yaml file::

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

    helm upgrade --cleanup-on-fail <hubname> jupyterhub/jupyterhub --namespace <hubname> --version 0.10.6 --timeout 600s --debug -f hub-configs/<hubname>.yaml -f ../../secrets/<hubname>.yaml
