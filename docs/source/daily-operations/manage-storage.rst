.. _manage-storage:

Managing Storage for Your Hub
===============================


Specifying Storage Size for a Hub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The JupyterHub helm charts set a default size for the storage (the ``PersistentVolumeClaim``) for a pod at 10GB. If you do not specify a storage size, your chart will use the default of 10GB per pod. To specify a different storage limit you can use:

.. code-block:: yaml

  singleuser:
    storage:
      capacity: 2Gi

Docs below
https://zero-to-jupyterhub.readthedocs.io/en/latest/customizing/user-storage.html#size-of-storage-provisioned



TODO: Add stuff here on storage

Changing Storage Limit for a Single Pod
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a user fills up their volume, the pod will fail to start (specifically, when
there is no storage remaining, the LifeCycleHook that fetches the data using
`nbgitpuller` will exit with non-zero status, causing the pod startup to fail).

You can resize the `PersistentVolumeClaim` for a single user, either from the
command line or from the GCloud browser console.

From the Command Line
---------------------

Get the list of persistent volume claims (PVCs)::

  $ kubectl get pvc -n <namespace>

The important column here is ``NAME``, which is the name of the PVC (which will be in the format <hubname/claim-username>)::

  NAME              STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
  claim-kcranston   Bound    pvc-5606e622-9b79-11ea-8c26-42010a80013d   16Gi       RWO            standard       13d
  claim-lwasser     Bound    pvc-2c353c02-9647-11ea-97b9-42010a800008   10Gi       RWO            standard       19d
  hub-db-dir        Bound    pvc-a50dce14-962a-11ea-97b9-42010a800008   1Gi        RWO            standard       19d


(Optional) Get existing details about the claim::

  kubectl describe pvc <pvc-name> -n <namespace>

Edit the claim (this will open up the yaml file in your default text editor)::

  kubectl edit pvc <pvc-name> -n <namespace>

When you edit the pvc, you will edit the size in the `spec` section of the yaml::

  spec:
    accessModes:
    - ReadWriteOnce
    resources:
      requests:
        storage: 15Gi
    storageClassName: standard
    volumeMode: Filesystem
    volumeName: pvc-1a469296-abb3-11e8-804b-42010a8000a9


.. note::

  You can only make PV's bigger, not smaller. If you try to make them smaller you
  will get an error that looks something like:
  `error: persistentvolumeclaims "claim-lwasser" is invalid`.


Save your changes, and check the new limit::

  kubectl describe pvc claim-kcranston -n ea-hub

You will see the message "Waiting for user to (re-)start a pod to finish file
system resize of volume on node." An admin user can stop the user's pod with
the JupyterHub admin interface at https://hub.earthdatascience.org/<hubname>/hub/admin.
The next time the user logs in, they will have the re-sized volume.

Check Pod Storage Capacity
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To check the capacity and availability of storage for a pod, you can use terminal
on the JupyterHub. `df -h` (h for human readable) will allow you to see both
available storage and what has been used by the pod::

  df -h

The /home/jovyan is your user directory. So focus on that line to determine how
much storage is available on a pod::

  Filesystem      Size  Used Avail Use% Mounted on
  overlay          95G   22G   74G  23% /
  tmpfs            64M     0   64M   0% /dev
  tmpfs            15G     0   15G   0% /sys/fs/cgroup
  /dev/sde        9.8G   38M  9.8G   1% /home/jovyan
  /dev/sda1        95G   22G   74G  23% /etc/hosts
  shm              64M     0   64M   0% /dev/shm
  tmpfs            15G     0   15G   0% /proc/acpi
  tmpfs            15G     0   15G   0% /proc/scsi
  tmpfs            15G     0   15G   0% /sys/firmware


.. note::
  For more on resizing pods read:
  https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/

From the GCloud Browser Interface
---------------------------------

#. Navigate to the `list of persistent volume claims <https://console.cloud.google.com/kubernetes/persistentvolumeclaim?project=ea-jupyter>`_
#. Click on the name of the claim that you want to edit (this will be called <claim-username>), making sure it is the right hub by checking the namespace column
#. Click the edit link
#. Edit the yaml and save.

TODO: Verify whether data is lost when you resize the PVC.

TODO: POD if full but you don't need the data -- delete it

TODO: POD IS full but you DO need the data -- add instructions for both somehow capturing the data and then deleting
