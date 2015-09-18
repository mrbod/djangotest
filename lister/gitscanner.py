#!/usr/bin/env python
import sys
import os
import os.path
import subprocess as sp

gitcmd = 'git rev-parse --show-toplevel'.split()

def _isgit(path, d):
    cwd = os.getcwd()
    os.chdir(os.path.join(path, d))
    try:
        devnull = open(os.devnull, 'w')
        try:
            r = sp.check_output(gitcmd, stderr=devnull).strip()
            tmp = os.getcwd()
            if os.path.realpath(r) == os.path.realpath(tmp):
                return True
        except Exception as e:
            sys.stderr.write('_isgit failed: {}\n'.format(str(e)))
            return False
        finally:
            devnull.close()
    finally:
        os.chdir(cwd)
    return False

def maybe_git(path, d):
    if os.path.isdir(os.path.join(path, d, '.git')):
        return True
    if os.path.isdir(os.path.join(path, d, 'refs')):
        return True
    return False

def isgit(path, d):
    #print 'path:', path
    #print 'd:', d
    if maybe_git(path, d):
        return _isgit(path, d)
    return False

class Repository(object):
    def __init__(self, name, info=''):
        self.name = name
        self.info = info

    def __str__(self):
        return '{0.name}\n\t{0.info}'.format(self)

def scan_away(base_path):
    repos = []
    for path, dirs, files in os.walk(base_path):
        subdirs = []
        for i, d in enumerate(dirs):
            if d.startswith('.'):
                continue
            elif isgit(path, d):
                print 'repo:', d
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

