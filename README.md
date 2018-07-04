# hub-ops
Infrastructure and operations for the Earthlab JupyterHub.

Deployment status: [![Build Status](https://travis-ci.org/earthlab/hub-ops.svg?branch=master)](https://travis-ci.org/earthlab/hub-ops)

## Day to day operations

Day to day operations are describe in [day-to-day](day-to-day.md).


## Available hubs

Hubs which are available for deployment:
* The main earthhub. This should always be running. It is configured via the
  chart in `earthhub/`.
* The test hub. This is a hub for experimenting with. It is configured via the
  chart in `staginghub/`.


## Initial setup

The first round of installing this deployment requires you to follow `setup.md`
and to install the contents of the `outer-edge/` directory and all additional
hubs you want to deploy.

bump
