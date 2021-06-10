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
* edit the hub's configuration in :code:`hub-configs/<hubname>.yaml`
* commit the change and make a PR
* fix any GitHub Action errors, https://github.com/earthlab/hub-ops/actions
* after merge, Actions will will start deploying your changes. Check the status of your deployment
* once the Actions workflows have completed, check that the hub is working as expected at https://hub.earthdatascience.org/hubname/.

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
2. (If GitHub authentication) Remove access tokens for the users
3. Manually delete storage <TODO: add more details about the best way to handle storage removal>


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

1. Make a PR that edits the Actions workflows in :code:`.github/workflows` and removes the hub from the hubname array (there is one instance in :code:`build-only` and two in :code:`build-deploy`).

Merge that PR. Wait for Actions to finish before moving on.

If you check your hub should still be running at this point. This is because all we have done is stop Actions from trying to build the docker image and deploy the hub when there are changes.

Step two: Uninstall the helm release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second step is to uninstall the helm release to shutdown
your hub. You will need :code:`kubectl` and :code:`helm` installed and configured
on your local machine to perform this step.

To check for the installation

One way to check this is to
run :code:`kubectl get pods --namespace=<hubname>`. You should see a few pods running::

  NAME                              READY   STATUS                  RESTARTS   AGE
  continuous-image-puller-hgrjp     1/1     Running                 0          4d9h
  hook-image-awaiter-zc8tv          1/1     Running                 0          4d11h
  hook-image-puller-tlmmz           0/1     Init:ImagePullBackOff   0          4d9h
  hub-c5c44d76b-k9lsb               1/1     Running                 0          4d10h
  proxy-5797f8d787-dm9fh            1/1     Running                 0          4d10h
  user-placeholder-0                1/1     Running                 0          4d9h
  user-placeholder-1                1/1     Running                 0          4d9h
  user-scheduler-779876497d-mcwgn   1/1     Running                 0          4d11h
  user-scheduler-779876497d-zvqbv   1/1     Running                 0          4d10h

But you should not see any pods named :code:`jupyter-username` (because this would indicate that users are still connected to your hub, and they might be surprised to be kicked off).

To check the helm releases currently installed, run :code:`helm list --all-namespaces`. It should look similar to this::


  NAME         	NAMESPACE    	REVISION	UPDATED                                	STATUS  	CHART               	APP VERSION
  cert-manager 	cert-manager 	1       	2021-01-11 10:19:55.227696 -0500 EST   	deployed	cert-manager-v1.1.0 	v1.1.0
  ea-hub       	ea-hub       	20      	2021-06-04 22:39:47.769249637 +0000 UTC	deployed	jupyterhub-0.10.6   	1.2.2
  ingress-nginx	ingress-nginx	1       	2021-01-11 10:53:04.954353 -0500 EST   	deployed	ingress-nginx-3.19.0	0.43.0
  nbgrader-hub 	nbgrader-hub 	22      	2021-06-04 22:39:55.101091107 +0000 UTC	failed  	jupyterhub-0.10.6   	1.2.2
  staginghub   	staginghub   	5       	2021-01-25 20:54:55.67648376 +0000 UTC 	deployed	jupyterhub-0.10.6   	1.2.2

Depending on how many hubs are running there will be at least two releases
deployed: :code:`ingress-nginx` and :code:`cert-manager`. These support
all hubs and should never be removed. In the case shown above there are three
hubs running: :code:`ea-hub`, :code:`nbgrader-hub` and :code:`staginghub`.

To uninstall the hub :code:`<hubname>` from the namespace <hubname> run::

    helm uninstall <hubname> -n <hubname>

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

Removing users from a hub
-------------------------

Removing users from a hub involves removing them from the whitelist and /or admin lists and also revoking their authentication token (if using GitHub authentication). This is because checking the whitelist is the last step in authentication, so if the user already has a token, the whitelist has no effect.

To remove users from the whitelist, edit :code:`hub-configs/hubname.yaml` and remove their usernames from the auth whitelist.

To revoke _all_ user tokens, you can go to the `Settings for the Earthlab GitHub organization <https://github.com/organizations/EarthLab/settings/applications>`_ and click `Revoke all user tokens`. This means that all users will need to re-authenticate (and will be checked through the whitelist).

To revoke a single user token, you can probably do this via the GitHub API directly but we have not tried this yet.
