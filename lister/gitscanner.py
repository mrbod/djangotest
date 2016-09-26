#!/usr/bin/env python
import sys
import os
import os.path
import subprocess as sp
from collections import namedtuple

gitcmd = 'git rev-parse --show-toplevel'.split()

Repository = namedtuple('Repository', 'name info')

def _isgit(target):
    cwd = os.getcwd()
    os.chdir(target)
    try:
        devnull = open(os.devnull, 'w')
        try:
            r = sp.check_output(gitcmd, stderr=devnull).strip()
            tmp = os.getcwd()
            if os.path.realpath(r) == os.path.realpath(tmp):
                return True
        except subprocess.CalledProcessError as e:
            sys.stderr.write('_isgit failed: {}\n'.format(str(e)))
            return False
        finally:
            devnull.close()
    finally:
        os.chdir(cwd)
    return False

def maybe_git(target):
    if os.path.isdir(os.path.join(target, '.git')):
        return True
    if os.path.isdir(os.path.join(target, 'refs')):
        return True
    return False

def isgit(target):
    if maybe_git(target):
        return _isgit(target)
    return False

def scan_away(base_path):
    repos = []
    for path, dirs, files in os.walk(base_path):
        subdirs = []
        for d in dirs:
            if d.startswith('.'):
                continue
            target = os.path.join(path, d)
            if isgit(target):
                repos.append(Repository(d, path))
            else:
                subdirs.append(d)
        dirs[:] = subdirs
    return repos

def scan_for_gits(base_path='.'):
    return scan_away(base_path)

if __name__ == '__main__':
    for r in scan_for_gits('.'):
        print r

