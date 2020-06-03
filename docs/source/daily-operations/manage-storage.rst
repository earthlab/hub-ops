.. _manage-storage:

Managing Storage for Your Hub
===============================


Storage Allocation: Specifying Storage size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default size for a hub pod is 10GB. if you do not specify this in your chart
then it will be 10GB. If you wish to specify the storage size you can use:

.. code-block:: yaml

  singleuser:
    storage:
      capacity: 2Gi

Docs below
https://zero-to-jupyterhub.readthedocs.io/en/latest/customizing/user-storage.html#size-of-storage-provisioned



TODO: Add stuff here on storage

If A Pod is Full
~~~~~~~~~~~~~~~~~


TODO: POD if full but you don't need the data -- delete it

TODO: POD IS full but you DO need the data -- add instructions for both somehow capturing the data and then deleting
