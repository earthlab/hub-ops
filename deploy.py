#!/usr/bin/env python3
import argparse
import logging
import subprocess
import os

logging.basicConfig(level=logging.INFO)


def helm(*args, **kwargs):
    logging.info("Executing helm %s", " ".join(args))
    return subprocess.check_call(["helm"] + list(args), **kwargs)


def kubectl(*args, **kwargs):
    logging.info("Executing kubectl %s", " ".join(args))
    return subprocess.check_call(["kubectl"] + list(args), **kwargs)


def docker(*args, **kwargs):
    logging.info("Executing docker %s", " ".join(args))
    return subprocess.check_call(["docker"] + list(args), **kwargs)


def capture_kubectl(*args, **kwargs):
    # capture the output of calling kubectl
    logging.info("Executing and capturing kubectl %s", " ".join(args))
    return subprocess.check_output(["kubectl"] + list(args), **kwargs)


def last_git_modified(path, n=1):
    """Get last revision at which `path` got modified"""
    return (
        subprocess.check_output(
            ["git", "log", "-n", str(n), "--pretty=format:%h", path]
        )
        .decode("utf-8")
        .split("\n")[-1]
    )


def get_next_image_spec(hubname, image_dir):
    """Build and return the name of the image to use, based on last commit"""
    if os.path.exists(image_dir):
        # get last image spec
        tag = last_git_modified(image_dir)
        image_name = "earthlabhubops/ea-k8s-user-" + hubname
        image_spec = image_name + ":" + tag
        print("Image spec is {}".format(image_spec))
        return image_spec
    else:
        print("No image spec")
        return None


def get_previous_image_spec(hubname, image_dir):
    """Pull latest available version of image to maximize cache use."""
    image_name = "earthlabhubops/ea-k8s-user-" + hubname
    try_count = 0
    # try increasingly older git revisions
    print("Try to pull older image to use in build with --cache-from")
    while try_count < 5:
        last_image_tag = last_git_modified(image_dir, try_count + 1)

        last_image_spec = image_name + ":" + last_image_tag
        try:
            docker("pull", last_image_spec)
            return last_image_spec

        except subprocess.CalledProcessError:
            try_count += 1
            pass

    return None

def image_exists(image_spec):
    try:
        docker("pull", image_spec)
        return True

    except subprocess.CalledProcessError:
        return False


# def build_hub_image(hubname, commit_range, push=False):
#     # Build and push to Docker Hub the hub(!) images that need updating
#     # from `hub-images/`
#     image_dir = "hub-images/" + hubname
#     # No work for us if there is no custom user image
#     if not os.path.exists(image_dir):
#         return
#
#     tag = last_git_modified(image_dir)
#     image_name = "earthlabhubops/ea-k8s-hub-" + hubname
#     image_spec = image_name + ':' + tag
#
#     needs_rebuilding = image_requires_build(image_dir, commit_range)
#
#     if needs_rebuilding:
#         previous_image_spec = get_previous_image_spec(image_name, image_dir)
#
#         if previous_image_spec is not None:
#             docker('build',
#                    '--cache-from', previous_image_spec,
#                    '-t', image_spec,
#                    image_dir)
#         else:
#             docker('build',
#                    '-t', image_spec,
#                    image_dir)
#
#         if push:
#             docker('push', image_spec)
#
#         print('build completed for hub image', image_spec)
#
#     else:
#         print('Do not need to rebuild hub image, using', image_spec)
#
#     return image_spec


def build_user_image(hubname, push=False):
    # Build and push to Docker Hub singleuser images that need updating
    # from `user-images/`
    image_dir = "user-images/" + hubname

    # get the image_spec based on the git commit that last modified image_dir
    image_spec = get_next_image_spec(hubname, image_dir)
    if image_spec is None:
        return

    # check whether the image already exists
    if image_exists(image_spec):
        print("Image {} exists; no need to rebuild".format(image_spec))

    else:
        print("Image {} does not exist; rebuilding".format(image_spec))
        previous_image_spec = get_previous_image_spec(hubname, image_dir)

        if previous_image_spec is not None:
            docker(
                "build",
                "--cache-from",
                previous_image_spec,
                "-t",
                image_spec,
                image_dir,
            )
        else:
            docker("build", "-t", image_spec, image_dir)
        print("Build completed for image", image_spec)

        if push:
            try:
                docker("push", image_spec)
                print("Pushed {} to dockerhub".format(image_spec))
            except subprocess.CalledProcessError:
                print("Failed to push {} to dockerhub".format(image_spec))

    return image_spec


def deploy(hubname):
    # monitoring chart isn't in the hub-charts directory
    if hubname != "monitoring":
        chart_dir = os.path.join("hub-charts", hubname)
    else:
        chart_dir = hubname
    extra_args = []

    # Check for a custom singleuser image
    image_dir = "user-images/" + hubname
    image_spec = get_next_image_spec(hubname, image_dir)
    # tag is the part after the ':'
    if image_spec is not None:
        print("Using", image_spec, "as user image for", hubname)
        tag = image_spec.split(":").pop()
        extra_args.extend(
            ["--set-string", "singleuser.image.tag={}".format(tag)]
        )

    # No longer have hub-image dir, but leaving this here in case
    # it gets resurrected in the future
    # Check for a custom hub image
    # hub_image_dir = "hub-images/" + hubname
    # if os.path.exists(hub_image_dir):
    #     tag = last_git_modified(hub_image_dir)
    #     image_name = "earthlabhubops/ea-k8s-hub-" + hubname
    #     image_spec = image_name + ':' + tag
    #
    #     print("Using", image_spec, "as hub image for", hubname)
    #     extra_args.extend(['--set-string',
    #                        'jupyterhub.hub.image.tag={}'.format(tag)])


    # add the jupyterhub helm chart repo
    jupyter_url = "https://jupyterhub.github.io/helm-chart/"
    helm_args = [ "repo", "add", "jupyterhub", jupyter_url]
    helm(*helm_args)

    # Update helm. The helm command is
    # helm upgrade --install <CHARTNAME> jupyterhub/jupyterhub \
    # --namespace <CHARTNAME> --version <VERSION> \
    # --timeout 600s -f hub-configs/<CHARTNAME>.yaml \
    # -f secrets/<CHARTNAME>.yaml --cleanup-on-fail --force --debug

    helm_release = hubname
    helm_chart = "jupyterhub/jupyterhub"
    jupyter_version = "0.10.6"

    # Assume hub-specific settings are in the file hub-configs/hubname.yaml
    # and secrets in secrets/hubname.yaml
    yamlfile = "{}.yaml".format(hubname)
    config_file = os.path.join("hub-configs",yamlfile)
    secrets_file = os.path.join("secrets", yamlfile)

    helm_args = [
        "upgrade",
        "--install",
        helm_release,
        helm_chart,
        "--namespace",
        hubname,
        "--version",
        jupyter_version,
        "--timeout",
        "600s",
        "-f",
        config_file,
        "-f",
        secrets_file,
        "--cleanup-on-fail",
        "--force",
        "--debug",
    ]

    helm_args += extra_args
    helm(*helm_args)


    logging.info("Checking that all deployments are up and running")
    kubectl_output = capture_kubectl("--namespace", hubname, "get", "deployments", "-o", "name")
    deployments = kubectl_output.decode().strip().split("\n")
    for d in deployments:
        name = d.split('/')[1]
        kubectl_args = [
            "rollout",
            "status",
            "--namespace",
            hubname,
            "deployment/{}".format(name)
            ]
        kubectl(*kubectl_args)


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "--build",
        help="Build user images",
        action="store_true",
    )
    argparser.add_argument(
        "--push",
        help="Push docker images to Docker Hub",
        action="store_true",
    )
    argparser.add_argument(
        "--deploy",
        help="Deploy hub",
        action="store_true",
    )
    argparser.add_argument(
        "hubname", help="Select which hub to deploy", choices=["ea-hub","nbgrader-hub"]
    )

    args = argparser.parse_args()

    if args.build:
        build_user_image(args.hubname, push=args.push)
        # build_hub_image(args.hubname, commit_range, push=args.push)

    if args.deploy:
        deploy(args.hubname)


if __name__ == "__main__":
    main()
