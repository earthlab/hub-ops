.. _deployment-workflow:

Deployment
==========

Deployment of the hubs is managed with continuous integration (TravisCI), rather than through use of the command-line kubernetes tools. Pull requests to the master branch trigger travis, as does merging a pull request. The Travis steps are scripted using python rather than calling :code:`kubectl` and :code:`helm` directly.


User workflow
-------------

When making changes to a hub (including both :ref:`new-hub` and :ref:`modify-remove-hub`), the expected workflow is:

* change the required settings in this repo (e.g. the helm charts in :code:`hub-charts`, or the Dockerfiles in :code:`user-images`)
* create a pull request with your changes - this will initiate a travis run that tests the builds of the docker image(s) and the docs. This does not push to Dockerhub, and does not deploy the hub. More specifically, this build `skips` the :code:`before_deploy` and :code:`deploy` sections in :code:`.travis.yml`.
* after the PR is merged, travis builds the docker image(s), pushes them to dockerhub, and deploys the hub(s). This build `runs` the :code:`before_deploy` and :code:`deploy` sections in :code:`.travis.yml`.

Before making changes to a production hub (i.e. one being used for a course), test your changes on :code:`staginghub` and only when that deploys correctly, copy these changes to the production hub.

Deploy script
-------------

The :code:`deploy.py` script at the top-level of this repo manages docker builds and deployments. The expectation is that this is only called by travis, not directly by the user (see the workflow, below).

Basic usage is :code:`python deploy.py chartname`. The following options are available:

* :code:`--no-setup` :  run without setup procedures (checking authentication to GCloud and docker, checking status of helm / tiller)
* :code:`--build` : build docker images; see :ref:`additional-hub-configuration` for setting these up
* :code:`--push` : push images to dockerhub (option ignored if build==False)
* :code:`--deploy` : deploy the hub

These are the commands that :code:`deploy.py` runs when deploying a hub :

.. code-block:: bash

  helm dependency update <chartname>
  helm upgrade --install --namespace <chartname> <chartname> <chart_dir> --force --wait --timeout 600 --cleanup-on-fail -f <secret>

Then, for each deployments found with :code:`kubectl -n <chartname> get deployments -o name`:

.. code-block:: bash

  kubectl rollout status --namespace <chartname> --watch <deployment>
