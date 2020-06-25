FROM earthlab/earth-analytics-python-env:f880467

# Install nbgrader server extensions - we only want the students to see the
# validate extension, but you can't just install one. You need to install
# them all and then disable the ones you don't want. Hmmm, ok.

# Setup nbgitpuller to sync files from course repo to hub
RUN conda install -c conda-forge nbgitpuller \
    && jupyter serverextension enable --py nbgitpuller --sys-prefix

# Setup nbzip - this allows students to download files from the hub
RUN pip install git+https://github.com/ryanlovett/jupyter-tree-download.git
