# hub-ops
Infrastructure and operations for the Earthlab JupyterHubs.

Deployment status: [![Build Status](https://travis-ci.org/earthlab/hub-ops.svg?branch=master)](https://travis-ci.org/earthlab/hub-ops)

## Documentation

Read the documentation at: https://earthlab-hub-ops.readthedocs.io/en/latest/index.html


## Available hubs

Hubs which are available for deployment:
* The main earthhub. This should always be running. It is configured via the
  chart in `earthhub/`.
* The test hub. This is a hub for experimenting with. It is configured via the
  chart in `staginghub/`.
