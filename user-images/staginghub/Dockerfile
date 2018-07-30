FROM earthlab/earth-analytics-python-env:41ae80f

RUN pip install --no-cache --upgrade --upgrade-strategy only-if-needed \
  jupyterhub==0.9.0 nbzip==0.0.4

RUN jupyter serverextension enable --py nbzip --sys-prefix
RUN jupyter nbextension install --py nbzip
RUN jupyter nbextension enable --py nbzip
