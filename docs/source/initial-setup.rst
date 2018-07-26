One time setup instructions
===========================

These are instructions for setting up from scratch and recreate the setup
that is assumed in all other parts of this documentation.

You should not need the instructions in this section very often.

A good guide, maintained by the JupyterHub team on how to setup a single
JupyterHub from zero is: `<https://zero-to-jupyterhub.readthedocs.io/en/latest/index.html>`_
Reading and following that guide once will help you understand more of this guide.


Create a project on Google cloud
--------------------------------

We assume you already did this or are using the Earthlab project. If you do not
have a project create one on `<https://console.cloud.google.com>`_.


Configure your gcloud and kubectl tools
---------------------------------------

To install the :code:`gcloud` command-line tool follow `step 3b of the z2jh guide <https://zero-to-jupyterhub.readthedocs.io/en/latest/google/step-zero-gcp.html>`_.

To install :code:`kubectl` (pronounced kube-cuddle) see `setp 4 of the z2jh guide <https://zero-to-jupyterhub.readthedocs.io/en/latest/google/step-zero-gcp.html>`_.

Make sure that you are talking to your newly created project. To list your
projects :code:`gcloud projects list`. Use the name from the PROJECT_ID column.
For example if your project is called :code:`ea-jupyter` run the following
command to set yourself up to use that project::

    gcloud config set project ea-jupyter


.. note::

    If you switch between different projects and clusters you might need this to
    switch to the right cluster. Not needed in the first run through.
    Setup for using the jhub cluster in the ea-jupyter project:

        gcloud container clusters get-credentials jhub --zone us-central1-b --project ea-jupyter


Create a cluster on google cloud
--------------------------------

Create a basic cluster::

    gcloud container clusters create jhub \
        --num-nodes=1 --machine-type=n1-standard-2 \
        --zone=us-central1-b --cluster-version=1.10.2-gke.3 \
        --enable-autoscaling --max-nodes=3 --min-nodes=1

Give your account super-user permissions needed to set up JupyterHub::

    kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user="<your google account email>"



Setup Helm
----------

Helm is the tool we use to manage "helm charts" which describe what we want to
have installed and running on the kubernetes cluster.

Full details on setting up helm: `<https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-helm.html#setting-up-helm>`_.

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
`config.yaml` you should instead edit `<hubname>/values.yaml`.

.. note::

    You will need to obtain the key to decrypt :code:`secrets/` somehow.
    Ask Tim Head or Leah Wasser.

After this follow the instructions in `outer-edge/READMEmd` to setup the
HTTP server that will route traffic to your hub. Without this your hub will not
be reachable from the internet.
