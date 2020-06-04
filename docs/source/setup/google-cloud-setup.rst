Google Cloud & Kubernetes Tools
===============================

Create a Project on Google cloud
--------------------------------

We assume you already did this or are using the Earth Lab project. If you do not
have a project create one on `<https://console.cloud.google.com>`_.

Configure Your gcloud and kubectl Tools
---------------------------------------

To install the :code:`gcloud` command-line tool follow `step 3b of the z2jh guide <https://zero-to-jupyterhub.readthedocs.io/en/latest/google/step-zero-gcp.html>`_.

To install :code:`kubectl` (pronounced kube-cuddle) see `setp 4 of the z2jh guide <https://zero-to-jupyterhub.readthedocs.io/en/latest/google/step-zero-gcp.html>`_.

Make sure that you are talking to your newly created project. To list your
projects use::

    gcloud projects list

Use the name from the PROJECT_ID column. For example if your project is
called :code:`ea-jupyter` run the following command to set yourself up to
use that project::

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


Create a Static IP
------------------

For a test deployment you can make do with a temporary IP. If you are setting
up a new long term public cluster, get a static IP.

To get one run::

    gcloud compute addresses create jhub-ip --region us-central1

and to see what value was assigned to it::

    gcloud compute addresses describe jhub-ip --region us-central1

and if you want to see what IP addresses were reserved for this project::

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
    Ask Leah Wasser, Max Joseph or Tim Head.

After this follow the instructions in ``outer-edge/README.md`` to setup the
HTTP server that will route traffic to your hub. Without this your hub will not
be reachable from the internet.
