Day to day operations
=====================

This document outlines how to perform typical tasks for the Earthlab hubs.


Making changes to an existing hub
---------------------------------

To make changes to an existing hub:

* create a new branch in your git repository
* edit the hub's configuration in :code:`<nameofthehub>/values.yaml`
* commit the change and make a PR
* once the PR is merged travis will deploy your changes
* check the status of your deployment and see what travis is doing by visiting:
  `<https://travis-ci.org/earthlab/hub-ops/branches>`_ Check the status of the latest
  build for the `master` branch
* once travis has deployed your changes, check by hand if everything is working
  as expected. If not, create a new PR that reverts your first PR. Then try again.


Creating a new hub
------------------

Each hub is configured by a "helm chart". A chart is a set of configuration files
written using YAML that describe the state we want the hub to be in. The deployment
tools then take care of making the real world correspond to our wishes.

Take a look at :code:`staginghub/` as an example chart to base yours on. A chart can
describe anything from a simple to a very complex setup. We typically use them
for low complexity things. The most important file is :code:`values.yaml` which is
where you configure your hub. Check the
`zero to JupyterHub guide <http://zero-to-jupyterhub.readthedocs.io/>`_
for ideas on what you might want to configure.

To create a new hub create a new directory with the same name as the hub you
want to have. Once your hub is up and running you will be able to reach it
at :code:`https://hub.earthdatascience.org/<hubname>`. You need to edit
:code:`jupyterhub.hub.baseUrl` in your :code:`values.yaml` and set it to the same name
as the directory (we will use :code:`<hubname>`). Remember the name has to be a part
of a valid URL. So you can't go completely crazy here.

You also need to configure the authentication setup.

You will need to add your hub in :code:`.travis.yml` so that it is tested and
automatically deployed.

Finally confgiuration values that need to remain secret can be stored in
:code:`secrets/<hubname>.yaml`.
