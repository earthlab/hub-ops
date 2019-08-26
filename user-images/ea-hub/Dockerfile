FROM earthlab/earth-analytics-python-env:81a8c26

RUN pip install --no-cache --upgrade --upgrade-strategy only-if-needed \
  nbzip==0.1.0 \
  https://github.com/data-8/nbgitpuller/archive/28fe9b1af2ba64b346d59bd13c99581346bf349f.zip

RUN pip install --no-cache --upgrade https://github.com/jupyter/notebook/archive/9d19aa3677a414341c5368622b01a2d229c2bad1.zip

RUN jupyter serverextension enable --py nbgitpuller --sys-prefix
RUN jupyter serverextension enable --py nbzip --sys-prefix
RUN jupyter nbextension install --py nbzip --sys-prefix
RUN jupyter nbextension enable --py nbzip --sys-prefix

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
