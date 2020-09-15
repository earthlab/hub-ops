# installing nbgrader and extensions on top of earthlab python env
FROM earthlab/earth-analytics-python-env:d53d66c

# Setup nbgitpuller to sync files from course repo to hub
RUN conda install -c conda-forge nbgitpuller \
    && jupyter serverextension enable --py nbgitpuller --sys-prefix

# Setup nbzip - this allows students to download files from the hub
RUN pip install git+https://github.com/ryanlovett/jupyter-tree-download.git

# install jupyterhub from conda-forge and update jupyter_console
RUN conda install -c conda-forge jupyterhub
RUN pip uninstall --yes jupyter-console
RUN conda install -c conda-forge jupyter_console=6.0.0

# Setup nbgrader + extensions
RUN jupyter nbextension install --sys-prefix --py nbgrader --overwrite \
    && jupyter nbextension enable --sys-prefix --py nbgrader \
    && jupyter serverextension enable --sys-prefix --py nbgrader

  # Install zip to support the download tool
  USER root
  RUN apt-get update && apt-get -y install zip
