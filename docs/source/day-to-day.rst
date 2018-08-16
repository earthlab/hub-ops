Day to day operations
=====================

This document outlines how to perform typical tasks for the Earth Lab, University
of Colorado Jupyter Hubs.


Monitoring
----------

To get an overview of the health of the hubs and infrastructure visit the
`Grafana page <https://grafana.hub.earthdatascience.org/>`_.

The ``Hub monitor`` page lets you see how many pods are running, launch success
rate, which users are using a lot of CPU, etc. For each hub separately.

The ``Node monitor`` page contains information about each of the compute nodes
that are part of the cluster.

The best way to use the monitoring is to watch it for a while when not a lot
is happening to get a feeling for what "baseline" looks like. Then login to
a hub and observe what it looks like on the monitoring. Next time a workshop
is happening keep an eye on the monitoring to see what happens when lots of
people login at the same time.


Operations
----------

This section contains commands and snippets that let you inspect the state of
the cluster and perform tasks that are useful when things are broken.

To perform these commands you need to have ``kubectl`` installed and setup
on your local laptop (see :ref:`google-cloud` for details).


Inspecting what is going on in the cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see what is running on the cluster (and get a feeling for what is the normal
state of affairs) run ``kubectl get pods --all-namespaces``. This will list all
pods that are running, including service pods that we don't ever interact with.

You should see at least two pods in each namespace that is associated to a hub.
The namespace and hubname are the same, so ``staginghub`` lives in the
``staginghub`` namespace.

Pods in the ``kube-system``, ``monitoring`` and ``router`` namespaces are best
left alone.

Each hub specific namespace should contain at least two pods: ``hub-77fbd96bb-dh2b5``
and ``proxy-6549f4fbc8-8zn67``. Everything after hub- and proxy- will change
when you restart the hub or make configuration changes. The status of these
two pods should be ``Running``.

To see what a pod is printing to its terminal run ``kubectl logs <podname> --namespace <hubname>``.
This will let you see errors or exceptions that happened.

You can find out more about a pod by running ``kubectl describe pod <podname> --namespace <hubname>``.
This will give you information on why a pod is not running or what it is up to
while you are waiting for it to start running.

When someone logs in to the hub and starts their server a new pod will appear in
the namespace of the hub. The pod will be named ``jupyter-<username>``. You can
inspect it with the usual ``kubectl`` commands.


Known problems and solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a known problem in one of JupyterHub's components that means sometimes
the hub misses that a user's pod has started and will keep that user waiting
after they logged in. The symptoms of this are that there is a running pod for
a user in the right namespace but the login process does not complete. In this
case restart the offending hub by running ``kubectl delete pod hub-... --namespace <hubname>``,
replacing the ... in the hub name with the proper name of the hub pod. This should
not interrupt currently active users and fixes a lot of things that can go wrong.


Inspecting virtual machines
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To tell how many virtual machines (or nodes) are part of the cluster run
``kubectl get nodes``. There should be at least one node with ``core-pool`` in
its name running at all times. Once users login and start their servers new
nodes will appear that have ``user-pool`` in their name. These nodes are
automatically created and destroyed based on demand.

You can learn about a node by running ``kubectl describe node <nodename>``.


Scaling up cluster before a class/workshop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Having a cluster that automatically scales up and down based on demand is great,
but starting a new virtual machine takes a few minutes (~5-9minutes). This makes
for a poor user experience when lots of users login at the start of a class or
workshop. Luckily in this case we know when the herd is going to arrive and can
scale up the cluster just before. To do this go to the admin panel of your hub
``https://hub.earthdatascience.org/<hubname>/hub/admin`` and start the servers
for a large fraction of your users. This will trigger the scale up event and if
you do this about 15minutes before the start of a class your cluster should be
big and ready when students login.

One thing to keep in mind is that unused user servers will eventually be turned
off again and the cluster will shrink down again. This means you can not scale
up the cluster using this strategy many hours before class starts.


Making changes to an existing hub
---------------------------------

To make changes to an existing hub:

* fork https://github.com/earthlab/hub-ops
* in your fork create a new branch
* edit the hub's configuration in :code:`hub-charts/<nameofthehub>/values.yaml`
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

All the hub deployments are based on the `Zero to JupyterHub guide
<http://zero-to-jupyterhub.readthedocs.io/>`_
(`GitHub repository <https://github.com/jupyterhub/zero-to-jupyterhub-k8s>`_).
The guide provides excellent advice on configuring your hub as well as a helm
chart that we use. Each of the hubs here can use a different version of the
Z2JH helm chart. This raises two questions: which version should I use and how
do I find out what versions are available?

All versions of the JupyterHub helm charts are available from `<https://jupyterhub.github.io/helm-chart/>`_.
We are currently using a `development release <https://jupyterhub.github.io/helm-chart/#development-releases-jupyterhub>`_
of the chart for most hubs. The reason for this is that a lot of new features
have been added but no new release has been made (should happen in August 2018).
If you do not know better picking the latest development release is a good choice.

To change the version of the hub that you are using edit :code:`hub-charts/<hubname>/requirements.yaml`.
The below snippet shows how to use :code:`v0.7-578b3a2`:

.. code-block:: yaml

    dependencies:
    - name: jupyterhub
      version: "v0.7-578b3a2"
      repository: "https://jupyterhub.github.io/helm-chart"

You can also inspect what version :code:`hub-charts/staginghub/requirements.yaml` is
using. Unless there are security related fixes or bugs that hinder your use of
a specific version of a chart the recommendation is to not update your chart
version during a workshop. Over the course of a semester it might be worth
upgrading to the latest version, but should mostly be avoided.

Take a look at :code:`staginghub/` as an example chart to base yours on. A chart can
describe anything from a simple to a very complex setup. We typically use them
for low complexity things. The most important file is :code:`values.yaml` which is
where you configure your hub. Check the
`zero to JupyterHub guide <http://zero-to-jupyterhub.readthedocs.io/>`_
for ideas on what you might want to configure.

Step one: Create a new hub directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To begin your hub creation, first create a new directory in ``hub-charts/``
with the name that you'd like your hub to have. The hub name should end with
the word :code:`hub`.

You need to edit
:code:`jupyterhub.hub.baseUrl` in your :code:`values.yaml` and set it to the same name
as the directory (we will use :code:`yourhubname-hub`). The hub name will become a
part of the hub URL, so pick a name wisely!

Example:

.. code-block:: yaml

    jupyterhub:
      hub:
        baseUrl: /yourhubname-hub/

Step two: Setup authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Next decide how you'd like to authenticate your hub. You can use Github,
Google or a "hash" based authenticator.
Read more about :ref:`authentication`.

Step three: Update the travis build so it recognizes the new hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step in removing a hub is to turn it off. To do this

1. Open the  :code:`travis.yml` file in the root of the hub-ops repo.
2. Remove the commands listed below

In the :code:`scripts` section remove:

.. code-block:: yaml

    - |
      # Build bootcamp-hub
      python ./deploy.py --no-setup --build bootcamp-hub

In the :code:`before_deploy` section remove:

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
