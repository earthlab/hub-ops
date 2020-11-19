.. _grafana_and_prometheus:

Grafana and Prometheus
======================

The `monitoring <https://github.com/earthlab/hub-ops/tree/master/monitoring>`_ hub implements a graphical display of hub resource usage at  `<https://grafana.hub.earthdatascience.org/>`_. This uses the open source projects `Grafana <https://grafana.com/>`_  and `Prometheus <https://prometheus.io/>`_. Prometheus collects, stores, and provides time series data about the hub operations. Grafana plots the data.

We include helm charts for Grafana and Prometheus, and then there are additional settings (resource, etc) in values.yml. There are additional settings available through the Grafana web interface.

Editing the Grafana hub list
----------------------------

When you add or remove hubs, the Grafana pages does not automatically update with the new hub list (there is probably a way to do this, but that's a project for another day). To modify the list of hubs available, you modify the settings in the web interface.

To log in to Grafana from the `monitoring page <https://github.com/earthlab/hub-ops/tree/master/monitoring>`_, click the little arrow + box icon in the bottom right corner of the screen:

  .. image:: ../media/login-icon.png
        :width: 200

The username is ``admin`` and the password is in ``secrets/monitoring.yml``. You can also retreive secrets using ``kubectl``. Username::

   $ kubectl get secrets -n monitoring monitoring-grafana -o jsonpath='{.data.admin\-user}' | base64 -D

and password::

   $ kubectl get secrets -n monitoring monitoring-grafana -o jsonpath='{.data.admin\-password}' | base64 -D

Once logged in, click on the settings (gear) icon at the top of the page. Go to the `Variables` tab, and modify the list for `$hubname`. Save your changes.
