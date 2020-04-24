Daily Operations
================

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
