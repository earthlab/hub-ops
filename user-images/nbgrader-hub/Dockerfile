# installing nbgrader and extensions on top of earthlab python env
FROM earthlab/earth-analytics-python-env:eeb6a3b

# install jupyterhub from conda-forge and update jupyter_console
RUN conda install -c conda-forge jupyterhub
RUN pip uninstall jupyter-console
RUN conda install -c conda-forge jupyter_console=6.0.0

# install nbgrader from git to get not-yet-merged partial credit branch
RUN pip install --upgrade \
  git+https://github.com/kcranston/nbgrader.git@partial_credit

RUN jupyter nbextension install --sys-prefix --py nbgrader --overwrite
RUN jupyter nbextension enable --sys-prefix --py nbgrader
RUN jupyter serverextension enable --sys-prefix --py nbgrader

# then uninstall everything but the validate extension
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
