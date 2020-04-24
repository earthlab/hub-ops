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

IMPORTANT: you must close and reopen the terminal after installing gcloud
command line tool for it to recognize the gcloud command that you need to install
kubernetes locally.


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

Once you have installed help, close and reopen your terminal window for it to
be properly recognized. Then, you can verify that you have the correct version
and that helm installed properly by running:

    .. code:: bash

        helm version

It should provide output like:

    .. code-block:: bash

        Client: &version.Version{SemVer:"v2.9.1", GitCommit:"20adb27c7c5868466912eebdf6664e7390ebe710", GitTreeState:"clean"}
        Server: &version.Version{SemVer:"v2.9.1", GitCommit:"20adb27c7c5868466912eebdf6664e7390ebe710", GitTreeState:"clean"}


Setting up git-crypt
--------------------

The files in :code:`secrets/` are encrypted with `git-crypt <https://www.agwa.name/projects/git-crypt/>`_.
This allows
us to store sensitive information in the repository "in plain sight". Travis
knows how to decrypt these files and by the end of this section so will you.

1. install :code:`git-crypt`. On OSX `brew install git-crypt` will work or follow
   the isntructions on https://www.agwa.name/projects/git-crypt/
2. obtain a copy of :code:`hub-ops.gitcrypt.key`. You can ask Leah Wasser or Max
   Joseph for a copy. Copy the file into your checkout of :code:`hub-ops`
3. from the checkout directory run :code:`cat hub-ops.gitcrypt.key | git-crypt unlock -`
   or :code:`git-crypt unlock hub-ops.gitcrypt.key`. You should now be able to
   see plain text files in :code:`secrets/`.
4. Add your name to the list of people to contact in step 2.

Done.
