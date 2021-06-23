.. _new-hub:

==================
Deploying New Hubs
==================

Each hub is configured by a "helm config file" that lives in :code:`hub-configs`. These files append or replace values on top of the JupyterHub helm chart.

All the hub deployments are based on the `Zero to JupyterHub guide
<http://zero-to-jupyterhub.readthedocs.io/>`_
(`GitHub repository <https://github.com/jupyterhub/zero-to-jupyterhub-k8s>`_).
The guide provides excellent advice on configuring your hub as well as a helm
chart that we use.

Step one: Pick a name for your hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For deployment to work correctly, all steps here must use consistent hub naming with the same spelling, punctuation, etc. Once deployed, the hub will be publicly available at https://hub.earthdatascience.org/<hubname>. Pick a name wisely!

Step one: Create a new hub config file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On a new git branch, create a new config file in :code:`hub-configs/`. The simplest way is to copy one of the existing files::

  $ cp hub-configs/ea-hub.yaml hub-configs/<hubname>.yaml

The name of the new file must be <hubname>.yaml.

The parts that you must update are::

.. code-block:: yaml

  hub:
    baseUrl: /<hubname>/

  singleuser:
    image:
      name: earthlabhubops/ea-k8s-user-<hubname>
      tag: set-on-deployment

If you want the contents of a github repository to be available in the user's home directory on startup (for example, a course materials repo), edit this part, otherwise remove it::

.. code-block:: yaml

    lifecycleHooks:
      postStart:
        exec:
          command: ["gitpuller", "<repo-url>", "<branch>", "<dir-to-clone-into>"]

Check the
`Zero to JupyterHub guide <http://zero-to-jupyterhub.readthedocs.io/>`_
for ideas on what you might want to configure.

Step two: Create a secrets file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Based on the `z2jh instructions <https://zero-to-jupyterhub.readthedocs.io/en/latest/jupyterhub/installation.html#prepare-configuration-file>`_, create a file called :code:`<hubname>.yaml` in the :code:`secrets` directory. Then create a random hex string as a security token for the hub (requires that the openssl package be installed on your local machine)::

  openssl rand -hex 32

Copy the output and paste into the :code:`secrets/<hubname>.yaml` file::

.. code-block:: yaml

  proxy:
    secretToken: "<RANDOM_HEX>"

Save the file. This will be automatically encrypted by git-crypt and stored securely on GitHub.

Step three: Setup authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next decide how you'd like to authenticate your hub. You can use Github,
Google or a "hash" based authenticator.
Read more about :ref:`authentication`.


Step four: Set up a Docker image for the hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To customize the Docker image used for your hub (for example, the python environment or specific operating system or python packages), create a Dockerfile for the hub::

# Create a <hubname> directory in :code:`user-images`
# Create a Dockerfile for the hub (probably easiest to copy one from another hub and modify as needed)

The Docker image will be built and pushed to Dockerhub automatically by GitHub Actions once you create (and merge) the pull request. 

Step five: Update GitHub Actions to build the hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use GitHub Actions to build the docker image and deploy the hub. To include your new hub, add it to the :code:`hubname` array in the `build-only <https://github.com/earthlab/hub-ops/blob/main/.github/workflows/build-only.yml>_` and `build-deploy <https://github.com/earthlab/hub-ops/blob/main/.github/workflows/build-deploy.yml>`_ workflows::

.. code-block:: yaml

    strategy:
          matrix:
            hubname: [ea-hub, nbgrader-hub]

.. note::

    The `hubname` array needs to be updated in the single job in `build-only` and in both jobs in `build-deploy`, i.e. in three places total.

Step six: Update the deploy.py script with the hub name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally you need to list your :code:`<HUBNAME>` as a valid chartname that
:code:`deploy.py` recognises by editing permitted values of the :code:`chartname`
argument:

.. code-block:: python

    argparser.add_argument(
        'chartname',
        help="Select which chart to deploy",
        choices=['earthhub', 'nbgrader-hub', '<HUBNAME>']
    )

Configuration values that need to remain secret can be stored in
:code:`secrets/<hubname>.yaml`.

Step six: Submit and merge a pull request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Commit your changes (on a feature branch, not on :code:`main`!), make a PR, wait for the basic tests to run,
check that Actions built at your new hub configuration, then merge the PR. The hub will not deploy until after the merge.

Once your hub is up and running you will be able to reach it
at :code:`https://hub.earthdatascience.org/<hubname>`.

JupyterHub version
------------------

Each of the hubs on the :code:`main` branch use the same version of the
Z2JH helm chart. This is specified in the :code:`helm upgrade` command in `deploy.py`. If you want to test out a new version without affecting existing hubs, try out your changes on the :code:`staging` branch. See :ref:`deployment-workflow` for details on the staging branch.

All versions of the JupyterHub helm charts are available from `<https://jupyterhub.github.io/helm-chart/>`_.
We are generally use the latest stable release. The JupyterHub [heml chart changelog](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CHANGELOG.md) has all of the details about changes between versions.

Unless there are security related fixes or bugs that hinder your use of
a specific version of a chart, we recommend not modifying the chart
version during a workshop. Over the course of a semester it might be worth
upgrading to the latest version, but should mostly be avoided.
