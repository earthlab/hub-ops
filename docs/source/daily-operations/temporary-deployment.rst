.. _tempdeploy:

Deployment on the new cluster
=============================

These are temporary instructions for configuring and deploying hubs on the
new cluster. (Temporary as we get GitHub Actions set up to do this
automatically).

The two hubs are available at https://hub.earthdatascience.org/ea-hub and
https://hub.earthdatascience.org/nbgrader-hub

GCloud setup
------------

We've created a new GKE cluster called :code:`jhub2`. To set up authentication
to the new cluster::

    gcloud container clusters get-credentials jhub2

Now this cluster will be the default for all :code:`gcloud`, :code:`kubectl`,
and :code:`helm` commands that you run locally.

If your authentication still seems messed up, you can delete the hidden
:code:`.kube` directory in your home directory and re-run the get-credentials
command.

Hub configuration
-----------------

The configuration files for the hubs are now in a directory called
:code:`hub-configs` (NOT in :code:`hub-charts`). There is one file per hub
rather than a subdirectory for each hub. The deployment script expects these
to be named '':code:`hubname.yaml`.

Docker configuration
--------------------

This has not changed. There is a subdirectory for each hub under
:code:`user-images`. Edit the dockerfile as needed and commit your changes. 

Deployment
----------

To build and push Docker images, and to deploy the hub, use the
:code:`deploy.py` script.

.. note::
    Make sure you have committed any changes to the Dockerfiles, as the
    script looks at the last commit to determine the tag and whether
    re-building is required!

To build the image only::

    $ python deploy.py --build <hubname>

To build and push to Dockerhub (push only works in concert with --build)::

    $ python deploy.py --build --push <hubname>

After successfully building and pushing::

    $ python deploy.py --deploy <hubname>
