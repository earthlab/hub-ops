#!/usr/bin/env python3
import argparse
import logging
import subprocess
import yaml
import os


def helm(*args, **kwargs):
    logging.info("Executing helm", ' '.join(args))
    return subprocess.check_call(['helm'] + list(args), **kwargs)


def kubectl(*args, **kwargs):
    logging.info("Executing kubectl", ' '.join(args))
    return subprocess.check_call(['kubectl'] + list(args), **kwargs)


def capture_kubectl(*args, **kwargs):
    # capture the output of calling kubectl
    logging.info("Executing kubectl", ' '.join(args))
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


def deploy(chartname):
    helm('dep', 'up', cwd=chartname)

    install_args = ['upgrade', '--install',
                    '--namespace', chartname,
                    chartname,
                    chartname,
                    '--force',
                    '--wait',
                    '--timeout', '600',
                    '-f', os.path.join('secrets', f'{chartname}.yaml')
                    ]
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
        'chartname',
        help="Select which chart to deploy",
        choices=['staginghub', 'earthhub', 'monitoring']
    )

    args = argparser.parse_args()

    if args.run_setup:
        setup_auth()
        setup_helm()

    deploy(args.chartname)


if __name__ == '__main__':
    main()
