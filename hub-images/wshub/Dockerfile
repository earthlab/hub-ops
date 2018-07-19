# If you make big updates to the chart version used by wshub
# you probably want to bump up the tag here as well to avoid
# the chart and hub image drifting apart
FROM jupyterhub/k8s-hub:f8dec3f

USER root
RUN pip3 install --no-cache-dir \
         jupyterhub-hashauthenticator==0.4.0

USER ${NB_USER}
