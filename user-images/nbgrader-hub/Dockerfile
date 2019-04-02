# installing nbgrader and extensions on top of earthlab python env
FROM earthlab/earth-analytics-python-env:41ae80f

RUN pip install --no-cache --upgrade --upgrade-strategy only-if-needed \
  jupyterhub==0.9.6 \
  nbgrader==0.5.5

RUN jupyter nbextension install --sys-prefix --py nbgrader --overwrite
RUN jupyter nbextension enable --sys-prefix --py nbgrader
RUN jupyter serverextension enable --sys-prefix --py nbgrader
