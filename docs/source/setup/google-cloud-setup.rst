Google Cloud & Kubernetes Tools
===============================

Create a Project on Google cloud
--------------------------------

We assume you already did this or are using the Earth Lab project. If you do not
have a project create one on `<https://console.cloud.google.com>`_.

Configure Your gcloud and kubectl Tools
---------------------------------------

Install the :code:`gcloud` command-line tool and the :code:`kubectl` component as per steps 1-3 of the `z2jh GKE guide <https://zero-to-jupyterhub.readthedocs.io/en/latest/kubernetes/google/step-zero-gcp.html>`_.

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
    Setup for using the jhub2 cluster in the ea-jupyter project:

        gcloud container clusters get-credentials jhub2 --zone us-central1-b --project ea-jupyter


Create a cluster on google cloud
--------------------------------

Create a basic cluster::

  gcloud container clusters create jhub2 \
      --num-nodes=1 --machine-type=n1-standard-2 \
      --zone=us-central1-b --image-type=cos_containerd \
      --enable-autoscaling --max-nodes=3 --min-nodes=1

Here, we are using the default version of kubernetes rather than specifying a version. You can see the default version of kubernetes using :code:`gcloud container get-server-config`. When :code:`jhub2` was created, the defaultVersion on the RELEASE channel is 1.17.13-gke.2600.

We also use the containerd image type rather than the default cos type because the latter is being deprecated, see https://cloud.google.com/kubernetes-engine/docs/concepts/using-containerd.

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

We deviate from the guide in that we run multiple JupyterHubs on one cluster, each hub in its own namespace. The config file for each hub is in the :code:`hub-configs` directory. So, when the z2jh guide asks you to edit
``config.yaml`` you should instead edit ``hub-configs/<hubname>.yaml``.

.. note::

    You will need to obtain the key to decrypt :code:`secrets/` somehow.
    See :ref:`git-crypt` for details. 

After this follow the instructions in ``outer-edge/README.md`` to setup the
HTTP server that will route traffic to your hub. Without this your hub will not
be reachable from the internet.
