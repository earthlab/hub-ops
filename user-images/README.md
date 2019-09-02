# Docker images used to customise the user's environment

This folder contains the `Dockerfile`s needed to build the image in which a
user runs. Use this if you want to make specific `Python` libraries available
to your users or install additional kernels.

Each hub has its own image.

If you want to customize the environment that the hub itself runs in `hub-images/`
instead.

`earthenv-user` is an image that contains the Earth Analytics Python
environment. The source of this conda environment  is maintained here:
https://github.com/earthlab/earth-analytics-python-env


## Automated builds

Unfortunately we can not use Docker Hub for building these as we need them to
be ready when we deploy the hub(s) that use them. Instead we build them on
travis and then push to Docker Hub. The tooling is in `deploy.py`
