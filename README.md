[![DOI](https://zenodo.org/badge/136452806.svg)](https://zenodo.org/badge/latestdoi/136452806)

# Multiple Hub Deployment for Earth Lab JupyterHubs | hub-ops

Infrastructure and operations for the Earth Lab JupyterHubs.

Deployment status: [![Build Status](https://travis-ci.org/earthlab/hub-ops.svg?branch=master)](https://travis-ci.org/earthlab/hub-ops)
Documentation status: [![Docs Status](https://readthedocs.org/projects/earthlab-hub-ops/badge/?version=latest)](https://readthedocs.org/projects/earthlab-hub-ops/builds/)

## Documentation

Read the documentation at: https://earthlab-hub-ops.readthedocs.io/en/latest/index.html

Build the documentation locally using:

`make html`

## Monitoring

Visit https://grafana.hub.earthdatascience.org/ for monitoring of the hubs.


## Available hubs

Hubs which are running:
* The [earth analytics course hub](https://hub.earthdatascience.org/ea-hub/).
  It is configured via the chart in `hub-charts/ea-hub/`.
* The [test hub](https://hub.earthdatascience.org/staginghub/). This is a hub
  for experimenting with. It is configured via the chart in `hub-charts/staginghub/`.
* The [earth data science corps hub](https://hub.earthdatascience.org/edsc-hub/), configured using the chart in `hub-charts/edsc-hub/`

Hubs available for deployment (currently not running):

* The [nbgrader hub](https://hub.earthdatascience.org/nbgrader-hub). This is a
  hub that uses a development version of nbgrader while we wait for a PR to be
  merged into the base repo. It is configured using  the chart in
  `hub-charts/nbgrader-hub/`.
* The [workshop hub](https://hub.earthdatascience.org/wshub/). It is configured
  via the chart in `hub-charts/wshub/`. Used for a 45 person workshop with temporary logins.
* The [bootcamp hub](https://hub.earthdatascience.org/bootcamp-hub/).
    It is configured via the chart in `hub-charts/bootcamp-hub/`.


## Development

TODO: Add instructionst o build the docs locally here
