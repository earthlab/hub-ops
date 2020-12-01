.. _hub-monitoring:

Monitoring the Hubs
===================

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

For more about the our Grafana setup, see :ref:`grafana_and_prometheus`.

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
The namespace and hubname are the same, so an ``eahub`` hub lives in the
``eahub`` namespace.

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
