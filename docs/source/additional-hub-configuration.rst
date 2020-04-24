Customize Your Hub
==================

This is a collection of snippets and pointers to further customize your hub.


Custom user image
-----------------

Each hub can have a different environment, set of libraries and tools that is
provided to students. Hub's have a default user image, but it does not contain
many tools useful for doing science. However you can use it to test the rest
of your hub's setup.

The `Jupyter docker stacks <https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html>`_
provide a good collection of user images to start from. They are maintained by
the Jupyter team and updated reasonably often. They already work with JupyterHub
so you can quickly get going. Take a look at `the relationship between images <https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#image-relationships>`_
to get an idea of how the images relate to each other and what is installed
in each.

To configure your hub to use the `datascience-notebook <https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-datascience-notebook>`_
image edit your :code:`hub-charts/<hubname>/values.yaml` and add the following snippet:

.. code-block:: yaml

    jupyterhub:
      singleuser:
        image:
          name: jupyter/datascience-notebook
          tag: 135a595d2a93
        startTimeout: 600

You have to specify both the name and an explicit tag. You can not use :code:`latest`
as tag.

Pulling images from docker hub can be a bit slow at times. This means it is a
good idea to increase the :code:`startTimeout` to 600 seconds as shown above.


Self-made user image
--------------------

Sometimes none of the images available as part of the docker-stacks is enough
and you want to build a custom image. A good way to get started with this is
to base your work on a docker-stacks image that does most of what you need
and then customise it further. If you need the libraries from the
:code:`earth-analytics-python-env` you can start from that Docker image as
well.

To create a self-made user image create a new directory in the
:code:`user-images/` directory that has the same name as your hub.

In this directory place a :code:`Dockerfile`. This will be automatically
built by travis. To allow travis to find images and determine which need
rebuilding when you need to follow this naming convention.

Below an example of a minimally modified earth-analytics-python-env
docker image. It picks a specific tag of the earth-analytics-python-env and
then installs JupyterHub version 0.9.2. It also installs the `nbzip <https://github.com/data-8/nbzip>`_
notebook extension that lets students download the contents of their JupyterHub
home directories as a ZIP file to their local machine. The three commands that
install and enable the extension are typical for notebook extensions.

.. code-block:: shell

    FROM earthlab/earth-analytics-python-env:41ae80f

    RUN pip install --no-cache --upgrade --upgrade-strategy only-if-needed \
      jupyterhub==0.9.2 nbzip==0.1.0

    RUN jupyter serverextension enable --py nbzip --sys-prefix
    RUN jupyter nbextension install --py nbzip --sys-prefix
    RUN jupyter nbextension enable --py nbzip --sys-prefix

This image will be automatically built by travis. You will need to adjust your
hub's :code:`values.yaml` to use this image:

.. code-block:: yaml

    jupyterhub:
      singleuser:
        image:
          # tag will be set by travis on deployment
          name: earthlabhubops/ea-k8s-user-<hubname>
          tag: set-on-deployment
        startTimeout: 600

By following the convention that the custom user image for your hub is placed in
:code:`user-images/<hubname>` your docker image will be called :code:`earthlabhubops/ea-k8s-user-<hubname>`.
You do not have to set the tag by hand, travis will take care of that for you.

Pulling images from docker hub can be a bit slow at times. This means it is a
good idea to increase the :code:`startTimeout` to 600 seconds as shown above.


Prefetching data
----------------

It can be worth prefetching data for your students and including it directly
in the docker image. This means they will not have to wait when the course
starts. The downside is that your docker image gets bigger. Unfortunately we
can not directly add data to student's home directories. We can only bake this
data into the docker image used for each user. In this example we also setup
the necessary steps for the data to be copied over to each student's home
directory when they log into the hub.

To include data in your docker image create a custom user image for your hub
by following `Self-made user image`_.

An example of using :code:`earthpy` to download the :code:`spatial-vector-lidar`
dataset is given below:

.. code-block:: shell

    # Have to explicitly change the matplotlib backend in order to use
    # earthpy on the command line.
    RUN python -c "import matplotlib; matplotlib.use('Agg'); import earthpy; data = earthpy.io.EarthlabData('/data'); data.get_data('spatial-vector-lidar')"

The general idea is to execute a Python command to trigger the download and
store the results in :code:`/data`. You could use any kind of command to do this.
For example you could use :code:`wget` to fetch a dataset from FigShare or
any other website. Try out your command locally to make sure it does exactly
what you think it should do.

You can place the data in almost any location inside the container. By convention
we use :code:`/data` though.

If all you need is that the data is available in the container then you are done
now. If you'd like to also copy the data over to the students home directory
read the below snippet:

.. code-block:: yaml

    jupyterhub:
      singleuser:
        lifecycleHooks:
          postStart:
            exec:
              command:
                - "sh"
                - "-c"
                - >
                  mkdir -p /home/jovyan/earth-analytics/data;
                  rsync --ignore-existing -razv --progress /data/ /home/jovyan/earth-analytics/data;

The :code:`lifecycleHooks` entry in the :code:`values.yaml` of your hub give
you the option to run commands when a user's pod starts. You can place any
command here. Keep in mind that the user can start interacting with their pod
already before these commands complete. This means you want commands in this
section to run reasonably quickly. Otherwise users might be confused or interfere
with the commands here.

The above snippet does two things: it makes sure that the :code:`earth-analytics/data`
directory exists in the users home directory. After that it uses :code:`rsync`
to copy the data from :code:`/data` to this directory. The way :code:`rsync` is
configured means that it will not overwrite files that already exist in the user's
home directory. The assumption is that a user might have edited these files and
does not want them to be overwritten. If users want to refresh their datasets
because they broke something they can delete that file or dataset, stop their
server, and then restart it. They should now have the latest version of the
data again. Or they can run the above :code:`rsync` command manually.


.. _self-made-hub-image:

Self-made hub image
-------------------

You can customise the image and environment in which the JupyterHub itself runs.
This is useful when you want to use custom authenticators. To create a custom
hub image create a directory called :code:`hub-images/<hubname>`.

An example of installing the Hash authenticator is given here:

.. code-block:: shell

    # the tag given here has to be compatible with the version of the
    # helm chart you are using for this hub.
    FROM jupyterhub/k8s-hub:f8dec3f

    USER root
    RUN pip3 install --no-cache-dir \
             jupyterhub-hashauthenticator==0.4.0

    USER ${NB_USER}

This image will be automatically built by travis. You will need to adjust your
hub's :code:`values.yaml` to use this image:

.. code-block:: yaml

    jupyterhub:
      hub:
        image:
          # tag will be set by travis on deployment
          name: earthlabhubops/ea-k8s-hub-<hubname>
          tag: set-on-deployment

By following the convention that the custom hub image for your hub is placed in
:code:`hub-images/<hubname>` your hub's docker image will be called :code:`earthlabhubops/ea-k8s-hub-<hubname>`.
You do not have to set the tag by hand, travis will take care of that for you.


Custom authentication
---------------------

To configure the authentication mechanism read :ref:`authentication`.
