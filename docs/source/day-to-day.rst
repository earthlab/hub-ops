Day to day operations
=====================

This document outlines how to perform typical tasks for the Earth Lab, University
of Colorado Jupyter Hubs.


Monitoring
----------

To get an overview of the health of the hubs and infrastructure visit the
`Grafana page <https://grafana.hub.earthdatascience.org/>`_.

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

Step one: Create a new hub directory
~~~~~~~~~~~~

To begin your hub creation, first create a new directory with the name that you'd
like your hub to have. The hub name should end with the word :code:`hub`.

You need to edit
:code:`jupyterhub.hub.baseUrl` in your :code:`values.yaml` and set it to the same name
as the directory (we will use :code:`<hubname>`). The hub name will become a
part of the hub URL, so pick a name wisely!

Example:

.. code-block:: yaml
    jupyterhub:
      hub:
        baseUrl: /yourhubname-hub/

Step two: Setup authentication
~~~~~~~~~~~~
Next decide how you'd like to authenticate your hub. You can use Github,
Google or a "hash" based authenticator. Read more about that here
`Read more about that here <https://earthlab-hub-ops.readthedocs.io/en/latest/>`_

Step three: Update the travis build so it recognizes the new hub
~~~~~~~~~~~~

Next, you need to update  Travis (CI) instructions to test and
automatically deploy the new hub. In the root directory of the hub-ops repo, look
for the file: :code:`.travis.yml` Add a new step to the :code:`script` section
AFTER all of the other listed hubs, but before the documentation step:

.. code-block:: yaml

    - |
      # Build <HUBNAME
      python ./deploy.py --no-setup --build <HUBNAME>

You also need to add your hub to the :code:`before_deploy` section of the same
file:

.. code-block:: yaml

    - |
      # Stage 3, Step XXX: Deploy the <HUBNAME>
      python ./deploy.py --build --push --deploy <HUBNAME>

Step four: Update the deploy.py file with the hub name
~~~~~~~~~~~~

Finally you need to list your :code:`<HUBNAME>` as a valid chartname that
:code:`deploy.py` recognises by editing permitted values of the :code:`chartname`
argument:

.. code-block:: python

    argparser.add_argument(
        'chartname',
        help="Select which chart to deploy",
        choices=['staginghub', 'earthhub', 'wshub', 'monitoring', '<HUBNAME>']
    )

Configuration values that need to remain secret can be stored in
:code:`secrets/<hubname>.yaml`.

Commit your changes to a new branch, make a PR, wait for the basic tests to run,
check that travis looked at your new hub configuration, then merge the PR.

Once your hub is up and running you will be able to reach it
at :code:`https://hub.earthdatascience.org/<hubname>`.


Removing a hub
--------------

At the end of a workshop or semester you should consider removing a hub again.
While a hub scales down to use minimal resources when no one is logged in, it
does use some resources (like disk space) that will only be reclaimed once the
hub has been turned off.

Currently this is a manual process and requires you to have :code:`kubectl`
and :code:`helm` installed on your computer (see :ref:`google-cloud` and
:ref:`helm`). The reasoning is
that removing a hub involves deleting user data, which might be catastrophic!
So think about what you are doing and wait
for a quiet moment. A few extra days of paying for storage is going to be a lot
cheaper than trying to recreate data or code you deleted by accident.


Step one: Turn off your hub autobuild / update
~~~~~~~~~~~~

The first step in removing a hub is to turn it off. To do this

1. Open the  :code:`travis.yml` file in the root of the hub-ops repo.
2. Remove the commands listed below

In the :code:`scripts` section remove:

.. code-block:: yaml
    - |
      # Build bootcamp-hub
      python ./deploy.py --no-setup --build bootcamp-hub

In the :before_deploy:`scripts` section remove:
.. code-block:: yaml
      - |
        # Stage 3, Step 2: Deploy the earthhub
        python ./deploy.py --build --push --deploy bootcamp-hub

These two sections deploy your hub. There should be two commands for your
hub that look similar. Once you have removed these sections, create a pull request
in github. Merge that PR. Wait for travis
to deploy your changes before moving on.

If you check your hub should still be running at this point. This is because all
we have done so far is tell travis to not deploy new changes for this hub.


Step two: Uninstall the helm release
~~~~~~~~~~~~

The second step is to uninstall the helm release to shutdown
your hub. You will need :code:`kubectl` and :code:`helm` installed and configured
on your local machine to perform this step.

To check for the installation

One way to check this is to
run :code:`kubectl get pods --namespace=<hubname>`. This should show that there are
two pods running::

    NAME                     READY     STATUS    RESTARTS   AGE
    hub-7f575d6dc9-6x96c     1/1       Running   0          3d
    proxy-84b647bfc6-hgjx8   1/1       Running   0          10d

If there are more pods running or these two are not running you might be looking
at the wrong cluster or hub name. If you only see two pods with names starting
with :code:`hub-` and :code:`proxy-` you are probably good to go.

To check that your :code:`helm` command is properly configured run :code:`helm list`.
This will list all helm releases that are currently installed. It should look
similar to this::

    NAME      	REVISION	UPDATED                 	STATUS  	CHART               	NAMESPACE
    earthhub  	24      	Thu Jul 26 16:53:46 2018	DEPLOYED	earthhub-0.1.0      	earthhub
    ingress   	2       	Tue Jul  3 18:09:46 2018	DEPLOYED	nginx-ingress-0.22.1	router
    lego      	1       	Thu Jun 21 16:19:50 2018	DEPLOYED	kube-lego-0.4.2     	router
    monitoring	28      	Thu Jul 26 16:54:03 2018	DEPLOYED	monitoring-0.1.0    	monitoring
    staginghub	25      	Thu Jul 26 16:53:30 2018	DEPLOYED	staginghub-0.1.0    	staginghub
    wshub     	18      	Thu Jul 26 16:54:11 2018	DEPLOYED	wshub-0.1.0         	wshub

Depending on how many hubs are running there will be at least three releases
deployed: :code:`ingress`, :code:`lego`, and :code:`monitoring`. These support
all hubs and should never be removed. In the case shown above there are three
hubs running: :code:`staginghub`, :code:`wshub` and :code:earthhub`.

To delete the :code:`wshub` run :code:`helm delete wshub --purge`. If you now
visit :code:`https://hub.earthdatascience.org/<hubname>/` you should get a 404 error.

The final step is to delete all storage and IP addresses associated to your hub.
If you execute the next step there is no way to recover the data in student's
home drives or any other data associated to the cluster. Take a moment to make
sure you have all the data you will need from the cluster. To remove (without
chance of undoing it) all storage run the following command:
:code:`kubectl delete namespace <hubname>`.
