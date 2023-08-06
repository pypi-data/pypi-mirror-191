#!/usr/bin/python
import os
import sys
import subprocess as sp
import re

POSSIBLE_REMOTES = ['origin', 'upstream']

def get_primary_remote():
    try:
        stdout, stderr = sp.Popen(
            ['git', 'remote'], stdout=sp.PIPE, stderr=sp.PIPE, text=True).communicate()
    except (ValueError, OSError) as exc:
        print("Error while getting name of the remote: {}".format(exc))
        raise exc
    for remote in POSSIBLE_REMOTES:
        if remote in stdout:
            return remote
    return stdout.splitlines()[0]


def get_default_branch(remote):
    try:
        stdout, stderr = sp.Popen(
            ['git', 'remote', 'show', remote],
            stdout=sp.PIPE, stderr=sp.PIPE, text=True).communicate()
    except (ValueError, OSError) as ex:
        print("Error while getting remote master branch: {}".format(ex))
        raise ex
    branch = re.findall(r'HEAD branch:.*', stdout)
    branch = branch[0].split(' ')[-1]
    return branch

def _no_unstaged(status):
    unstaged_str = 'Changes not staged for commit:'
    if unstaged_str not in status:
        return True

def updateRepo(repodir, log_path='.repoupdater.log'):
    remote = get_primary_remote()
    master_branch = get_default_branch(remote=remote)
    os.chdir(repodir)

    log_path = '{}/{}'.format(repodir, log_path)

    print(
        "Updating {} branch of {} from remote {}".format(master_branch, repodir, remote))

    with open(log_path, mode='w') as log:
        stdout, stderr = sp.Popen(
            ['git', 'status'], stdout=sp.PIPE, stderr=sp.PIPE, text=True).communicate()
        log.write('\n'.join([stdout, stderr]) + os.linesep)
        if stderr == '' and _no_unstaged(stdout):
            stdout, stderr = sp.Popen(
                'git checkout {branch}'.format(branch=master_branch).split(' '),
                stdout=sp.PIPE, stderr=sp.PIPE, text=True).communicate()
            log.write('\n'.join([stdout, stderr]) + os.linesep)
            stdout, stderr = sp.Popen(
                'git remote update'.split(' '),
                stdout=sp.PIPE, stderr=sp.PIPE, text=True).communicate()
            log.write('\n'.join([stdout, stderr]) + os.linesep)
            stdout, stderr = sp.Popen(
                'git pull --ff-only'.split(' '),
                stdout=sp.PIPE, stderr=sp.PIPE, text=True).communicate()
            log.write('\n'.join([stdout, stderr]) + os.linesep)
        else:
            print(stdout, stderr)

def main(repo=os.getcwd(), logfile='.repoupdater.log'):

    updateRepo(repo, log_path=logfile)

if __name__ == '__main__':
    repo_path = os.getcwd()
    if len(sys.argv) == 2:
        main(repo_path, sys.argv[2])
