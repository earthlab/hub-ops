Day to day operations
=====================

This document outlines how to perform typical tasks for the Earthlab hubs.


Monitoring
----------

To get an overview of the health of the hubs and infrastructure visit the
`Grafana page <https://grafana.hub.earthdatascience.org/`_.

The `Hub monitor` page lets you see how many pods are running, launch success
rate, which users are using a lot of CPU, etc. For each hub separately.

The `Node monitor` page contains information about each of the compute nodes
that are part of the cluster.

The best way to use the monitoring is to watch it for a while when not a lot
is happening to get a feeling for what "baseline" looks like. Then login to
a hub and observe what it looks like on the monitoring. Next time a workshop
is happening keep an eye on the monitoring to see what happens when lots of
people login at the same time.


Making changes to an existing hub
---------------------------------

To make changes to an existing hub:

* fork https://github.com/earthlab/hub-ops
* in your fork create a new branch
* edit the hub's configuration in :code:`<nameofthehub>/values.yaml`
* commit the change and make a PR
* fix any errors travis finds
* once you merge the PR travis will start deploying your changes
* check the status of your deployment and see what travis is doing by visiting:
  `<https://travis-ci.org/earthlab/hub-ops/branches>`_ Check the status of the latest
  build for the `master` branch
* once travis has deployed your changes, check by hand if everything is working
  as expected by visiting :code:`https://hub.earthdatascience.org/<nameofthehub>/`.
  If something is broken, create a new PR that reverts your first PR. Then try
  again with a new PR.


Creating a new hub
------------------

Each hub is configured by a "helm chart". A chart is a set of configuration files
written using YAML that describe the state we want the hub to be in. After you
create a new chart describing a hub configuration and merge it, travis will
take care of making the real world correspond to your wishes.

Take a look at :code:`staginghub/` as an example chart to base yours on. A chart can
describe anything from a simple to a very complex setup. We typically use them
for low complexity things. The most important file is :code:`values.yaml` which is
where you configure your hub. Check the
`zero to JupyterHub guide <http://zero-to-jupyterhub.readthedocs.io/>`_
for ideas on what you might want to configure.

To create a new hub create a new directory with the same name as the hub you
want to have. It should end in :code:`hub`.

You need to edit
:code:`jupyterhub.hub.baseUrl` in your :code:`values.yaml` and set it to the same name
as the directory (we will use :code:`<hubname>`). Remember the name has to be a part
of a valid URL. So you can't go completely crazy here.

You also need to configure the authentication setup.

You will need to add your hub in :code:`.travis.yml` so that it is tested and
automatically deployed.

Finally confgiuration values that need to remain secret can be stored in
:code:`secrets/<hubname>.yaml`.

Once your hub is up and running you will be able to reach it
at :code:`https://hub.earthdatascience.org/<hubname>`.
