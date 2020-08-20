#!/usr/bin/env python3

import argparse
import subprocess

from nbgitpuller import GitPuller

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        'url',
        help="URL of the repo",
    )
    argparser.add_argument(
        'branch',
        help="Desired branch",
    )
    argparser.add_argument(
        'localdir',
        help="Name of the local repo directory",
    )

    args = argparser.parse_args()

    try:
        puller = GitPuller(args.url, args.branch, args.localdir)
        # I don't really understand why this iterator construct is necessary
        # Copied from nbgitpuller tests; without the loop it does not throw
        # exception when it fails
        for l in puller.pull():
            print(l)
    except subprocess.CalledProcessError as err:
        print(err)
