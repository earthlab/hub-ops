# Docker images used for these hubs

This folder contains the `Dockerfile`s needed to build images used by
all the hubs.

`earthenv-user` is an image that contains the Earthlab Analytics Python
environment. The source of which is mainted here: https://github.com/earthlab/earth-analytics-python-env


## Automated builds

Unfortuantely we can not use Docker Hub for building these as we need them to
be ready when we deploy the hub(s) that use them. Instead we build them on
travis and then push to Docker Hub. The tooling is in `deploy.py`
