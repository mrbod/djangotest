#!/usr/bin/env python
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from .models import Entry
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

def base_and_parent(path):
    if path.endswith('/'):
        parent = ''
        base = path
    else:
        if path.count('/') > 1:
            parent = path[:path.rfind('/')]
        else:
            parent = '/'
        base = path + '/'
    return base, parent

def dir_entries(base):
    git_list = []
    entry_list = []
    CWD = '.' + base
    for path, dirs, files in os.walk(CWD):
        for d in (x for x in dirs if not x.startswith('.')):
            if isgit(CWD, d):
                git_list.append(Entry(path=d,
                    description=os.path.realpath(os.path.join(CWD, d))))
            else:
                entry_list.append(Entry(path=d))
        break
    return git_list, entry_list

os.chdir('repos')

def index(request):
    base, parent = base_and_parent(request.path)
    git_list, entry_list = dir_entries(base)
    template = loader.get_template('lister/index.html')
    context = RequestContext(request,
            {
                'entry_list': entry_list,
                'git_list': git_list,
                'parent': parent,
                'base': base,
            }
        )
    return HttpResponse(template.render(context))

