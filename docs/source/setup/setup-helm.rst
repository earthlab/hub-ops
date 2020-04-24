Setup Helm 2.x
====================

Setup Helm Version 2.x
----------------------

Helm is the tool we use to manage "helm charts" which describe what we want to
have installed and running on the kubernetes cluster. This build requires helm
2.x to run properly

Full details on setting up helm: `<https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-jupyterhub/setup-helm.html>`_.

If you are having issues with installing helm version 2.x, the link below should
help:

Helm 2 Installation Tips: `<https://discourse.brew.sh/t/install-specific-version-of-kubernetes-helm/6342/4>`_.


After installing :code:`helm` locally, this is the abridged version of cluster side
things::

    kubectl --namespace kube-system create serviceaccount tiller
    kubectl create clusterrolebinding tiller \
            --clusterrole cluster-admin --serviceaccount=kube-system:tiller

    helm init --service-account tiller


Verify this worked by running :code:`helm version`. You might have to wait a
minute or two for this command to succeed. It should display something like::

    Client: &version.Version{SemVer:"v2.8.2", GitCommit:"a80231648a1473929271764b920a8e346f6de844", GitTreeState:"clean"}
    Server: &version.Version{SemVer:"v2.8.2", GitCommit:"a80231648a1473929271764b920a8e346f6de844", GitTreeState:"clean"}

Secure your helm setup::

    kubectl --namespace=kube-system patch deployment tiller-deploy --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'


Create a static IP
------------------

For a test deployment you can make do with a temporary IP. If you are setting
up a new long term public cluster, get a static IP.

To get one run::

    gcloud compute addresses create jhub-ip --region us-central1

and to see what value was assigned to it:

    gcloud compute addresses describe jhub-ip --region us-central1

and if you want to see what IP addresses were reserved for this project:

    gcloud compute addresses list


Install the JupyterHubs
-----------------------

`Full guide <https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-jupyterhub.html#setup-jupyterhub>`_.

We deviate a little from the guide in that we provide our own helm charts to
manage each JupyterHub deployment. In addition we deploy lots of support
infrastructure for monitoring, grading and the like.
The main thing to look out for is that when the z2jh guide asks you to edit
``config.yaml`` you should instead edit ``hub-charts/<hubname>/values.yaml``.

.. note::

    You will need to obtain the key to decrypt :code:`secrets/` somehow.
    Ask Tim Head or Leah Wasser.

After this follow the instructions in ``outer-edge/README.md`` to setup the
HTTP server that will route traffic to your hub. Without this your hub will not
be reachable from the internet.
