Additional ideas and snippets to customise your hub
===================================================

This is a collection of snippets and pointers to further customise your hub.


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
image edit your :code:`<hubname>/values.yaml` and add the following snippet:

.. code-block:: yaml

    jupyterhub:
      singleuser:
        image:
          name: jupyter/datascience-notebook
          tag: 135a595d2a93

You have to specify both the name and an explicit tag. You can not use :code:`latest`
as tag.


Self-made user image
--------------------

Some times none of the images available as part of the docker-stacks is enough
and you want to build a custom image. A good way to get started with this is
to base your work on a docker-stacks image that does most of what you need
and then customise it further. To do this create a new directory in the
:code:`user-images/` directory that has the same name as your hub.

In this directory we place a :code:`Dockerfile` which will be automatically
built by travis.



Prefetching data
----------------

It can be worth prefetching data for your students and including it directly
in the docker image. This means they will not have to wait when the course
starts. The downside is that your docker image gets bigger.

To include data in your docker image create a custom user image for your hub.
