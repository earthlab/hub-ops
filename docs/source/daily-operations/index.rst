================
Daily Operations
================

This section outlines how to perform typical tasks for the Earth Lab, University
of Colorado Jupyter Hubs.

There are different interfaces for the various operations. The instructions in :ref:`scaling` use the web-based adminstration panel, while the :ref:`hub-monitoring` is done via the command-line using `kubectl` and visually using  Grafana.

When you modify the hubs (including both :ref:`new-hub` and :ref:`modify-remove-hub`), deployment is triggered through continuous integration rather than directly using the command line tools. See :ref:`deployment-workflow` for details.

.. toctree::
   :maxdepth: 1
   :caption: Daily Operations

   scaling
   hub-monitoring
   new-hub
   modify-remove-hub
   deployment-workflow
   troubleshooting
