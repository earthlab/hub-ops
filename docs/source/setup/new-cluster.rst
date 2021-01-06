Setting up a new cluster
========================

These are notes from winter 2021 about setting up a new cluster from
scratch.

Resources
---------

* `setup pages <https://earthlab-hub-ops.readthedocs.io/en/latest/setup/google-cloud-setup.html>`_ for this project
* `z2jh documentation <https://zero-to-jupyterhub.readthedocs.io/en/latest/index.html>`_

Assumptions
-----------

* have a gcloud project :code:`ea-jupyter` and the gcloud command line tools set up
* have kubectl installed


Steps
-----

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
