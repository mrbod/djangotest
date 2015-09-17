#!/usr/bin/env python
import os
import os.path
import subprocess as sp

def isgit(path, d):
    if d.startswith('.'):
        return False
    cwd = os.getcwd()
    d = os.path.join(path, d)
    os.chdir(d)
    o = file('/dev/null', 'w')
    try:
        cmd = 'git rev-parse --show-toplevel'
        r = sp.check_output(cmd.split(), stderr=o).strip()
        tmp = os.getcwd()
        if os.path.realpath(r) == os.path.realpath(tmp):
            return True
    except:
        return False
    finally:
        os.chdir(cwd)
        o.close()
    return False

class Repository(object):
    def __init__(self, name, info=''):
        self.name = name
        self.info = info

for path, dirs, files in os.walk(os.getcwd()):
    subdirs = []
    for i, d in enumerate(dirs):
        if d.startswith('.'):
            continue
        elif isgit(path, d):
            print 'repo:', d
        else:
            subdirs.append(d)
    dirs[:] = subdirs

