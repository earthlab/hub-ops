.. _new-hub:

==================
Deploying New Hubs
==================

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
We are generally use the latest stable release. The JupyterHub [heml chart changelog](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/CHANGELOG.md) has all of the details about changes between versions.

To change the version of the hub that you are using edit :code:`hub-charts/<hubname>/requirements.yaml`.
The below snippet shows how to use :code:`v0.7-578b3a2`:

.. code-block:: yaml

    dependencies:
    - name: jupyterhub
      version: "v0.7-578b3a2"
      repository: "https://jupyterhub.github.io/helm-chart"

You can check `requirements.yml` file for other production hubs to see what version we are using elsewhere.

Unless there are security related fixes or bugs that hinder your use of
a specific version of a chart, we recommend not modifying the chart
version during a workshop. Over the course of a semester it might be worth
upgrading to the latest version, but should mostly be avoided.

Step one: Create a new hub directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To begin your hub creation, first create a new directory in ``hub-charts/``
with the name that you'd like your hub to have. The hub name should end with
the word :code:`hub`. Then, it is simplest to copy over the
:code:`Chart.yaml`, :code:`requirements.yaml`, and :code:`values.yaml` from
another hub and edit them as you need. Check the
`Zero to JupyterHub guide <http://zero-to-jupyterhub.readthedocs.io/>`_
for ideas on what you might want to configure.

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
      python ./deploy.py --build --push <HUBNAME>
      python ./deploy.py --deploy <HUBNAME>

Step four: Update the deploy.py file with the hub name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally you need to list your :code:`<HUBNAME>` as a valid chartname that
:code:`deploy.py` recognises by editing permitted values of the :code:`chartname`
argument:

.. code-block:: python

    argparser.add_argument(
        'chartname',
        help="Select which chart to deploy",
        choices=['earthhub', 'wshub', 'monitoring', '<HUBNAME>']
    )

Configuration values that need to remain secret can be stored in
:code:`secrets/<hubname>.yaml`.

Commit your changes to a new branch, make a PR, wait for the basic tests to run,
check that travis looked at your new hub configuration, then merge the PR.

Once your hub is up and running you will be able to reach it
at :code:`https://hub.earthdatascience.org/<hubname>`.
