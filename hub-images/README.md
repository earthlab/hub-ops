# Docker images used to customise the hub's environment

This folder contains the `Dockerfile`s needed to build the image in which a
hub runs. Use this if you want to add specific authenticators or other
custom tools to your JupyterHub.

Each hub can have its own image.

If you want to customize the environment a user sees look at `user-images/`
instead.

## Automated builds

Unfortuantely we can not use Docker Hub for building these as we need them to
be ready when we deploy the hub(s) that use them. Instead we build them on
travis and then push to Docker Hub. The tooling is in `deploy.py`
