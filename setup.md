# One time setup instructions

These are instructions for create a new JupyterHub with kubernetes on Google Cloud.

You probably don't need these every day, only when you want to create a new hub.

A good guide, maintained by the JupyterHub team on how to setup JupyterHub from
zero is: https://zero-to-jupyterhub.readthedocs.io/en/latest/index.html This
document is a condensed version of that guide.

## Create a project on Google cloud

We assume you already did this or are using the Earthlab project.


## Configure your gcloud and kubectl tools

To install the `gcloud` command-line tool follow [step 3b of the z2jh guide](https://zero-to-jupyterhub.readthedocs.io/en/latest/google/step-zero-gcp.html).

To install `kubectl` (pronounced kube-cuddle) see [setp 4 of the z2jh guide](https://zero-to-jupyterhub.readthedocs.io/en/latest/google/step-zero-gcp.html).

Make sure that you are talking to your newly created project. To list your
projects `gcloud projects list`. Use the name from the PROJECT_ID column.
If your project is called `ea-jupyter` run:

```
gcloud config set project ea-jupyter
```

---

### Note:

If you switch between different projects and clusters you might need this to
switch to the right cluster. Not needed in the first run through.
Setup for using the jhub cluster in the ea-jupyter project:
```
gcloud container clusters get-credentials jhub --zone us-central1-b --project ea-jupyter
```

---

## Create a cluster on google cloud

```
gcloud container clusters create jhub \
    --num-nodes=1 --machine-type=n1-standard-2 \
    --zone=us-central1-b --cluster-version=1.10.2-gke.3 \
    --enable-autoscaling --max-nodes=3 --min-nodes=1
```

Give your account super-user permissions needed to set up JupyterHub:
```
kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user="<your google account email>"
```


## Setup Helm

Helm is the tool we use to manage "helm charts" which describe what we want to
have installed and running on the kubernetes cluster.

Full details on setting up helm: https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-helm.html#setting-up-helm

After installing `helm` locally, this is the abridged version of cluster side
things:
```
kubectl --namespace kube-system create serviceaccount tiller
kubectl create clusterrolebinding tiller \
        --clusterrole cluster-admin --serviceaccount=kube-system:tiller

helm init --service-account tiller
```

Verify this worked with `helm version`. You might have to wait a minute or two
for this command to succeed. It should display something like:
```
Client: &version.Version{SemVer:"v2.8.2", GitCommit:"a80231648a1473929271764b920a8e346f6de844", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.8.2", GitCommit:"a80231648a1473929271764b920a8e346f6de844", GitTreeState:"clean"}
```

Secure your helm setup:
```
kubectl --namespace=kube-system patch deployment tiller-deploy --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'
```



## Create a static IP

For a test deployment you can make do with a temporary IP. If you are setting
up a new long term public cluster, get a static IP.

To get one run:
```
gcloud compute addresses create jhub-ip --region us-central1
```
and to see what value was assigned to it:
```
gcloud compute addresses describe jhub-ip --region us-central1
```
and if you want to see what IP addresses were reserved for this project:
```
gcloud compute addresses list
```


## Install JupyterHub

[Full guide](https://zero-to-jupyterhub.readthedocs.io/en/latest/setup-jupyterhub.html#setup-jupyterhub)

We deviate a little from the guide in that we provide our own helm chart to
manage to JupyterHub deployment. This makes it easier to add things to the
cluster, like a grading service or the like. The main thing to look out for
is that when the z2jh guide asks you to edit `config.yaml` you should instead
edit `earthhub/values.yaml`.

> You will need to obtain the key to decrypt `secrets/earthhub.yaml` somehow.
> Ask Tim Head or Leah Wasser.

Switch to the `earthhub` directory and run `helm dep up`, switch back to the
top level directory.

To install JupyterHub run:
```
helm install earthhub --name earthhub --namespace earthhub --version=v0.1.0 -f secrets/earthhub.yaml
```

The version has to match the version in `earthhub/Chart.yaml`.

After this follow the instructions in `outer-edge/READMEmd` to setup the
HTTP server that will route traffic to your hub. Without this your hub will not
be reachable from the internet.


## Making changes to an existing hub

To make changes to an existing hub:
* create a new branch in your git repository
* edit the hub's configuration in `<nameofthehub>/values.yaml`
* commit the change and make a PR
* once the PR is merged travis will deploy your changes
* check the status of your deployment and see what travis is doing by visiting: https://travis-ci.org/earthlab/hub-ops/branches Check the status of the latest
  build for the `master` branch
* once travis has deployed your changes, check by hand if everything is working
  as expected. If not, create a new PR that reverts your first PR. Then try again.

If you really want to (but you should never have to) you can deploy manually
from your local computer. The assumption is that if you are doing this you
have everything setup properly, so this command is just for reference:
```
helm upgrade --install --namespace earthhub earthhub earthhub --version=v0.1.0 -f secrets/earthhub.yaml
```
Yes, you need to type earthhub three times in a row 😀. It is the name of the
namespace, the name of the chart and the name of the deployment.
