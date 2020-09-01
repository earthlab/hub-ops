#!/usr/bin/env python3
import argparse
import logging
import subprocess
import yaml
import os

logging.basicConfig(level=logging.INFO)


def helm(*args, **kwargs):
    logging.info("Executing helm %s", ' '.join(args))
    return subprocess.check_call(['helm'] + list(args), **kwargs)


def kubectl(*args, **kwargs):
    logging.info("Executing kubectl %s", ' '.join(args))
    return subprocess.check_call(['kubectl'] + list(args), **kwargs)


def docker(*args, **kwargs):
    logging.info("Executing docker %s", ' '.join(args))
    return subprocess.check_call(['docker'] + list(args), **kwargs)


def capture_kubectl(*args, **kwargs):
    # capture the output of calling kubectl
    logging.info("Executing and capturing kubectl %s", ' '.join(args))
    return subprocess.check_output(['kubectl'] + list(args), **kwargs)


def setup_auth():
    """
    Set up GCloud + kubectl authentication for the Earthlab cluster
    """
    # Authenticate to GoogleCloud using our "travis-deployer" service account
    subprocess.check_output([
        "gcloud", "auth", "activate-service-account",
        "--key-file=secrets/gke-auth-key.json"
    ])

    # Use gcloud to populate ~/.kube/config, which kubectl / helm can use
    subprocess.check_call([
        "gcloud", "container", "clusters", "get-credentials",
        "jhub", "--zone=us-central1-b", "--project=ea-jupyter"
    ])


def setup_helm():
    """Ensure helm is up to date and ready to go"""
    subprocess.check_call([
        'helm', 'init', '--upgrade',
    ])
    # wait for tiller to come up
    subprocess.check_call([
        'kubectl', 'rollout', 'status',
        '--namespace', 'kube-system',
        '--watch', 'deployment', 'tiller-deploy',
    ])


def setup_docker():
    subprocess.check_output(['docker', 'login',
                             '-u', 'earthlabcu',
                             '-p', open("secrets/dockerhub").read().strip()])


def last_git_modified(path, n=1):
    """Get last revision at which `path` got modified"""
    return subprocess.check_output([
        'git',
        'log',
        '-n', str(n),
        '--pretty=format:%h',
        path
        ]).decode('utf-8').split('\n')[-1]

def get_next_image_spec(chartname, image_dir):
    """Build and return the name of the image to use, based on last commit"""
    if os.path.exists(image_dir):
        # get last image spec
        tag = last_git_modified(image_dir)
        image_name = "earthlabhubops/ea-k8s-user-" + chartname
        image_spec = image_name + ':' + tag
        return image_spec
    else:
        return None

def get_previous_image_spec(chartname, image_dir):
    """Pull latest available version of image to maximize cache use."""
    image_name = "earthlabhubops/ea-k8s-user-" + chartname
    try_count = 0
    # try increasingly older git revisions
    print("Try to pull older image to use in build with --cache-from")
    while try_count < 5:
        last_image_tag = last_git_modified(image_dir, try_count + 1)

        last_image_spec = image_name + ':' + last_image_tag
        try:
            docker('pull', last_image_spec)
            return last_image_spec

        except subprocess.CalledProcessError:
            try_count += 1
            pass

    return None


def image_requires_build(image_dir, commit_range=None):
    if commit_range is None:
        return False
    image_touched = subprocess.check_output([
        'git', 'diff', '--name-only', commit_range, image_dir,
    ]).decode('utf-8').strip() != ''

    return image_touched


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


def build_user_image(chartname, commit_range, push=False):
    # Build and push to Docker Hub singleuser images that need updating
    # from `user-images/`
    image_dir = "user-images/" + chartname
    image_spec = get_next_image_spec(chartname, image_dir)
    if image_spec is None:
        return

    needs_rebuilding = image_requires_build(image_dir, commit_range)

    if needs_rebuilding:
        previous_image_spec = get_previous_image_spec(chartname, image_dir)

        if previous_image_spec is not None:
            docker('build',
                   '--cache-from', previous_image_spec,
                   '-t', image_spec,
                   image_dir)
        else:
            docker('build',
                   '-t', image_spec,
                   image_dir)
        print('Build completed for image', image_spec)

        if push:
            try:
                docker('push', image_spec)
                print("Pushed {} to dockerhub".format(image_spec))
            except subprocess.CalledProcessError:
                print("Failed to push {} to dockerhub".format(image_spec))

    else:
        print('Do not need to rebuild image, using', image_spec)

    return image_spec


def deploy(chartname):
    # monitoring chart isn't in the hub-charts directory
    if chartname != 'monitoring':
        chart_dir = os.path.join('hub-charts', chartname)
    else:
        chart_dir = chartname
    extra_args = []

    # Check for a custom singleuser image
    image_dir = "user-images/" + chartname
    image_spec = get_next_image_spec(chartname, image_dir)
    # tag is the part after the ':'
    if image_spec is not None:
        print("Using", image_spec, "as user image for", chartname)
        tag = image_spec.split(':').pop()
        extra_args.extend(['--set-string',
                           'jupyterhub.singleuser.image.tag={}'.format(tag)])

    # No longer have hub-image dir, but leaving this here in case
    # it gets resurrected in the future
    # Check for a custom hub image
    # hub_image_dir = "hub-images/" + chartname
    # if os.path.exists(hub_image_dir):
    #     tag = last_git_modified(hub_image_dir)
    #     image_name = "earthlabhubops/ea-k8s-hub-" + chartname
    #     image_spec = image_name + ':' + tag
    #
    #     print("Using", image_spec, "as hub image for", chartname)
    #     extra_args.extend(['--set-string',
    #                        'jupyterhub.hub.image.tag={}'.format(tag)])

    helm('dep', 'up', cwd=chart_dir)

    install_args = ['upgrade', '--install',
                    '--namespace', chartname,
                    chartname,
                    chart_dir,
                    '--force',
                    '--wait',
                    '--timeout', '600',
                    '--cleanup-on-fail',
                    '-f', os.path.join('secrets', f'{chartname}.yaml')
                    ]
    install_args += extra_args
    helm(*install_args)

    logging.info(
        "Waiting for all deployments to be up and running"
        )
    deployments = capture_kubectl('--namespace', chartname,
                                  'get', 'deployments',
                                  '-o', 'name'
                                  ).decode().strip().split('\n')

    for d in deployments:
        kubectl('rollout', 'status',
                '--namespace', chartname,
                '--watch', d
                )


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--no-setup',
        help='Do not run setup procedures',
        dest='run_setup',
        action='store_false',
    )
    argparser.add_argument(
        '--build',
        help='Build user images',
        action='store_true',
    )
    argparser.add_argument(
        '--push',
        help='Push docker images to Docker Hub',
        action='store_true',
    )
    argparser.add_argument(
        '--deploy',
        help='Deploy chart',
        action='store_true',
    )
    # on staging branch, only staging hub allowed!
    argparser.add_argument(
        'chartname',
        help="Select which chart to deploy",
        choices=['staginghub']
    )

    args = argparser.parse_args()

    if args.run_setup:
        setup_auth()
        setup_helm()
        setup_docker()

    if args.build:
        commit_range = os.getenv('TRAVIS_COMMIT_RANGE')
        build_user_image(args.chartname, commit_range, push=args.push)
        # build_hub_image(args.chartname, commit_range, push=args.push)

    if args.deploy:
        deploy(args.chartname)


if __name__ == '__main__':
    main()
