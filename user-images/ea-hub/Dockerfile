FROM earthlab/earth-analytics-python-env:81a8c26

# Install nbgrader server extensions - we only want the students to see the
# validate extension, but you can't just install one. You need to install
# them all and then disable the ones you don't want. Hmmm, ok.

RUN jupyter nbextension install --sys-prefix --py nbgrader --overwrite
RUN jupyter nbextension enable --sys-prefix --py nbgrader
RUN jupyter serverextension enable --sys-prefix --py nbgrader

# disable create_assignment
RUN jupyter nbextension disable --sys-prefix create_assignment/main

# disable formgrader
RUN jupyter nbextension disable --sys-prefix formgrader/main --section=tree
RUN jupyter serverextension disable --sys-prefix \
  nbgrader.server_extensions.formgrader

# disable assignment_list
RUN jupyter nbextension disable --sys-prefix assignment_list/main --section=tree
RUN jupyter serverextension disable --sys-prefix \
  nbgrader.server_extensions.assignment_list
