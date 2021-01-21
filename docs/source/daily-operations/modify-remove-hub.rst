.. _modify-remove-hub:

===============================
Manage, Modify or Remove a Hub
===============================

These instructions are for modifying a JupyterHub. If you want to understand
more about how deployment works, or want to modify how we do deployment, see
:doc:`deployment </daily-operations/deployment-workflow>`.

Making Changes to an Existing Hub
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


Hub Maintanence
----------------

The JupyterHub interface has a built in administration panel that allows you to:

1. View users with access to the hub
2. View and manage active servers

It is important to note that this admin interface works well for a hub working
on a local server or virtual machine. However when running through Kubernetes
using Google Cloud (which is our current setup), most of the admin tasks will
need to be performed directly through kubernetes and google cloud rather than
in the admin interface.

Some features of the build in hub admin panel that will not work include the
ability to:

1. remove users and
2. shutdown the hub.

The above two steps should not be utilized in a Google Cloud deployment as
kubernetes is running behind the scenes and will thus control users and hub
deployment. To remove users you will thus need to

1. Edit the hub's yaml file which contains a list of users with permission to access the hub
2. Manually delete storage <TODO: add more details about the best way to handle storage removal>


Shut Down a Hub (And Remove Associated Storage)
-----------------------------------------------

At the end of a workshop or semester you should consider removing a hub again.
While a hub scales down to use minimal resources when no one is logged in, it
does use some resources (like disk space) that will only be reclaimed once the
hub has been turned off.

Currently this is a manual process and requires you to have :code:`kubectl`
and :code:`helm` installed on your computer (see :ref:`google-cloud-setup`). The reasoning is
that removing a hub involves deleting user data, which might be catastrophic!
So think about what you are doing and wait
for a quiet moment. A few extra days of paying for storage is going to be a lot
cheaper than trying to recreate data or code you deleted by accident.


Step one: Turn off your hub autobuild / update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step in removing a hub is to turn it off. To do this

1. Open the  :code:`travis.yml` file in the root of the hub-ops repo.
2. Remove the commands listed below

For example, to remove a hub called `bootcamp-hub`, in the :code:`scripts`
section remove:

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

  NAME        	REVISION	UPDATED                 	STATUS  	CHART               	APP VERSION	NAMESPACE
  cert-manager	2       	Wed Jun 17 10:36:47 2020	DEPLOYED	cert-manager-v0.15.1	v0.15.1    	cert-manager
  ea-hub      	19      	Fri Sep 18 14:01:53 2020	DEPLOYED	earthhub-0.1.0      	           	ea-hub
  edsc-hub    	2       	Wed Aug 26 21:26:46 2020	DEPLOYED	edsc-hub-0.1.0      	           	edsc-hub
  ingress     	3       	Tue Jul 31 06:23:04 2018	DEPLOYED	nginx-ingress-0.23.0	0.15.0     	router
  lego        	3       	Sun Oct 14 12:16:18 2018	DEPLOYED	kube-lego-0.4.2     	v0.1.6     	router
  monitoring  	162     	Fri Sep 18 14:02:34 2020	DEPLOYED	monitoring-0.1.0    	           	monitoring
  nbgrader-hub	7       	Fri Sep 18 14:00:24 2020	DEPLOYED	nbgrader-hub-0.1.0  	           	nbgrader-hub
  staginghub  	63      	Tue Sep 29 13:38:40 2020	DEPLOYED	staginghub-0.1.0    	           	staginghub

Depending on how many hubs are running there will be at least three releases
deployed: :code:`ingress`, :code:`cert-manager`, and :code:`monitoring`. These support
all hubs and should never be removed. In the case shown above there are four
hubs running: :code:`ea-hub`, :code:`edsc-hub`, :code:`nbgrader-hub` and :code:`staginghub`.

To delete the :code:`<hubname>` run::

    helm delete <hubname> --purge

If you now
visit :code:`https://hub.earthdatascience.org/<hubname>/` you should get a 404 error.

Step Three: Clean Up & Remove Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final step is to delete all storage and IP addresses associated with your hub.

IMPORTANT: If you execute the next step there is no way to recover the data in student's
home drives or any other data associated to the cluster. Take a moment to make
sure you have all the data you will need from the cluster.

To permanently remove all storage (**THERE IS NO RECOVERING THE DATA AFTER DOING
THIS!**) run the following command::

    kubectl delete namespace <hubname>

You have now deleted the hub and all of its storage.
