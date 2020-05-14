.. _deployment-workflow:

Deployment
==========

Deployment of the hubs is managed with continuous integration (travis), rather than through use of the command-line kubernetes tools. Pull requests to the master branch trigger travis, as does merging a pull request. Continuous integration is scripted using python rather than calling :code:`kubectl` and :code:`helm` directly. The high-level steps are:

#. Create pull request (travis skips :code:`before_deploy` and :code:`deploy` sections)

    #. Travis builds the docker images (but does not push to dockerhub)
    #. Travis builds the documentation

#. Merge pull request (travis runs the :code:`before_deploy` and :code:`deploy` sections)
    #. Travis builds docker images and pushes to dockerhub
    #. Travis deploys the hubs


Deploy script
-------------

The :code:`deploy.py` script at the top-level of this repo manages docker builds and deployments. The expectation is that this is only called by travis, not directly by the user (see the workflow, below).

Basic usage is :code:`python deploy.py chartname`. The following options are available:

* :code:`--no-setup` :  run without setup procedures (checking authentication to GCloud and docker, checking status of helm / tiller)
* :code:`--build` : build docker images; see :ref:`additional-hub-configuration` for setting these up
* :code:`--push` : push images to dockerhub (option ignored if build==False)
* :code:`--deploy` : deploys the hubs

The commands for deploying a hub :

.. code-block:: bash

  helm dependency update <chartname>
  helm upgrade --install --namespace <chartname> <chartname> <chart_dir> --force --wait --timeout 600 --cleanup-on-fail -f <secret>

User workflow
-------------
When making changes to the hub (including both :ref:`new-hub` and :ref:`modify-remove-hub`), the expected workflow is:

* change the required settings in this repo (e.g. the helm charts in `hub-charts`, or the Dockerfiles in `user-images`)
* create a pull request with your changes - this will test the builds of the docker image and docs
* upon merge of the PR, travis builds the docker images, pushes them to dockerhub, and deploys the hub(s)
