Installing admin tools
======================


.. _google-cloud:

Installing gcloud and kubectl
-----------------------------

There are several ways to install and use the gcloud command line tool. This
tool sends commands to Google Cloud and lets you do things like create
and delete clusters.

Two ways of installing gcloud::

    - Go to the `gcloud command line tool downloads page <https://cloud.google.com/sdk/downloads>`_
      to **download and install the gcloud command line tool**.
    - See the `gcloud documentation <https://cloud.google.com/pubsub/docs/quickstart-cli>`_ for
      more information on the gcloud command line tool.

Next install ``kubectl``, which is a tool for controlling kubernetes. From
the terminal, enter:

     .. code-block:: bash

        gcloud components install kubectl


.. _helm:

Installing helm
----------------

The simplest way to install helm is to run Helm's installer script at a
terminal:

   .. code:: bash

      curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash

`Alternative methods for helm installation <https://github.com/kubernetes/helm/blob/master/docs/install.md>`_
exist if you prefer to install without using the script.

Verify helm
~~~~~~~~~~~

You can verify that you have the correct version and that helm installed
properly by running:

    .. code:: bash

        helm version

It should provide output like:

    .. code-block:: bash

        Client: &version.Version{SemVer:"v2.9.1", GitCommit:"20adb27c7c5868466912eebdf6664e7390ebe710", GitTreeState:"clean"}
        Server: &version.Version{SemVer:"v2.9.1", GitCommit:"20adb27c7c5868466912eebdf6664e7390ebe710", GitTreeState:"clean"}
