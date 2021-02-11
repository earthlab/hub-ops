FROM earthlab/earth-analytics-python-env:1.1

# Install nbgrader server extensions - we only want the students to see the
# validate extension, but you can't just install one. You need to install
# them all and then disable the ones you don't want. Hmmm, ok.

# Setup nbgitpuller to sync files from course repo to hub
RUN conda install -c conda-forge nbgitpuller \
    && jupyter serverextension enable --py nbgitpuller --sys-prefix

# Setup nbzip - this allows students to download files from the hub
RUN pip install git+https://github.com/ryanlovett/jupyter-tree-download.git

# Setup nbgrader + extensions
RUN jupyter nbextension install --sys-prefix --py nbgrader --overwrite \
    && jupyter nbextension enable --sys-prefix --py nbgrader \
    && jupyter serverextension enable --sys-prefix --py nbgrader

# disable create_assignment & formgrader
RUN jupyter nbextension disable --sys-prefix create_assignment/main \
# disable formgrader
    && jupyter nbextension disable --sys-prefix formgrader/main --section=tree \
    && jupyter serverextension disable --sys-prefix \
  nbgrader.server_extensions.formgrader \
# disable assignment_list
    && jupyter nbextension disable --sys-prefix assignment_list/main --section=tree \
    && jupyter serverextension disable --sys-prefix \
  nbgrader.server_extensions.assignment_list

# Install zip to support the download tool
USER root
RUN apt-get update && apt-get -y install zip
