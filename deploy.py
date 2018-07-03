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
    subprocess.check_output([
        'helm', 'init', '--upgrade',
    ])
    # wait for tiller to come up
    subprocess.check_call([
        'kubectl', 'rollout', 'status',
        '--namespace', 'kube-system',
        '--watch', 'deployment', 'tiller-deploy',
    ])


def deploy(hubname):
    helm('dep', 'up', cwd=hubname)

    install_args = ['upgrade', '--install',
                    '--namespace', hubname,
                    hubname,
                    hubname,
                    '--force',
                    '--wait',
                    '--timeout', '600',
                    '-f', os.path.join('secrets', f'{hubname}.yaml')
                    ]
    helm(*install_args)

    logging.info(
        "Waiting for all deployments and daemonsets to be up and running"
        )
    deployments = kubectl('--namespace', hubname,
                          'get', 'deployments',
                          '-o', 'name'
                          ).decode().strip().split('\n')

    daemonsets = kubectl('--namespace', hubname,
                         'get', 'daemonsets',
                         '-o', 'name'
                         ).decode().strip().split('\n')

    for d in deployments + daemonsets:
        kubectl('rollout', 'status',
                '--namespace', hubname,
                '--watch', d
                )


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'hubname',
        help="Select which hub to deploy",
        choices=['staginghub', 'earthhub']
    )

    args = argparser.parse_args()

    setup_auth(args.hubname)
    setup_helm()
    deploy(args.hubname)


if __name__ == '__main__':
    main()
