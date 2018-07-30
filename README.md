# hub-ops
Infrastructure and operations for the Earthlab JupyterHubs.

Deployment status: [![Build Status](https://travis-ci.org/earthlab/hub-ops.svg?branch=master)](https://travis-ci.org/earthlab/hub-ops)
Documentation status: [![Docs Status](https://readthedocs.org/projects/earthlab-hub-ops/badge/?version=latest)](https://readthedocs.org/projects/earthlab-hub-ops/builds/)

## Documentation

Read the documentation at: https://earthlab-hub-ops.readthedocs.io/en/latest/index.html


## Monitoring

Visit https://grafana.hub.earthdatascience.org/ for monitoring of the hubs.


## Available hubs

Hubs which are running:
* The [main earthhub](https://hub.earthdatascience.org/earthhub/). This should
  always be running. It is configured via the chart in `earthhub/`.
* The [test hub](https://hub.earthdatascience.org/staginghub/). This is a hub
  for experimenting with. It is configured via the chart in `staginghub/`.

Hubs available for deployment (currently not running):
* The [workshop hub](https://hub.earthdatascience.org/wshub/). It is configured
  via the chart in `wshub/`. Used for a 45 person workshop with temporary logins.
