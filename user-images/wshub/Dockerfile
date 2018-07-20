FROM earthlab/earth-analytics-python-env:e8cc47d

RUN pip install --no-cache --upgrade --upgrade-strategy only-if-needed \
  jupyterhub==0.9.0

RUN pip install --no-cache git+https://github.com/data-8/nbgitpuller@28fe9b1af2ba64b346d59bd13c99581346bf349f
RUN jupyter serverextension enable --py nbgitpuller --sys-prefix

USER root
# Have to explicitly change the matplotlib backend in order to use
# earthpy on the command line.
RUN python -c "import matplotlib; matplotlib.use('Agg'); import earthpy; data = earthpy.io.EarthlabData('/data'); data.get_data('spatial-vector-lidar')"
USER $NB_UID

# a comment to trigger rebuilding
