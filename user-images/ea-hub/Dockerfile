FROM earthlab/earth-analytics-python-env:8d96000

RUN pip install --no-cache --upgrade --upgrade-strategy only-if-needed \
  jupyterhub==0.9.2 \
  nbzip==0.1.0 \
  https://github.com/data-8/nbgitpuller/archive/28fe9b1af2ba64b346d59bd13c99581346bf349f.zip

RUN jupyter serverextension enable --py nbgitpuller --sys-prefix
RUN jupyter serverextension enable --py nbzip --sys-prefix
RUN jupyter nbextension install --py nbzip --sys-prefix
RUN jupyter nbextension enable --py nbzip --sys-prefix
