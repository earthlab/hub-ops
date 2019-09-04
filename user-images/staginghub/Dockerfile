FROM earthlab/earth-analytics-python-env

# Install nbgrader server extensions - we only want the students to see the
# validate extension, but you can't just install one. You need to install
# them all and then disable the ones you don't want. Hmmm, ok.

# setup nbgitpuller to sync files
RUN conda install -c conda-forge nbgitpuller \
    && jupyter serverextension enable --py nbgitpuller --sys-prefix

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
