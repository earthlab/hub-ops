# Hub-configs

This directory contains the configuration files for the hubs. The values
specified here are applied on top of the jupyterhub helm chart using the
`-f` flag when calling `helm upgrade`.

There should be one file for each hub, and the deployment assumes that the
name of the config file matches the name of the hub, e.g. the config file for
`ea-hub` is called `ea-hub.yaml`.

Note that this is a change from the previous cluster setup, where each hub had
its own helm chart in the directory `hub-charts`. This new setup more closely
follows the zero-2-jupyterhub documentation.
