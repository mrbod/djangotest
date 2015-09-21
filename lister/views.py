#!/usr/bin/env python
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from .models import Entry
import os
import os.path
import gitscanner
from .forms import NewRepo

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
    CWD = './repos' + base
    print 'CWD', CWD
    for path, dirs, files in os.walk(CWD):
        for d in (x for x in dirs if not x.startswith('.')):
            if gitscanner.isgit(CWD, d):
                git_list.append(Entry(path=d,
                    description=os.path.realpath(os.path.join(CWD, d))))
            else:
                entry_list.append(Entry(path=d))
        break
    git_list.sort()
    entry_list.sort()
    return git_list, entry_list

def index(request):
    print request.path_info
    extra = request.get_host()
    base, parent = base_and_parent(request.path_info)
    git_list, entry_list = dir_entries(base)
    template = loader.get_template('lister/index.html')
    context = RequestContext(request,
            {
                'entry_list': entry_list,
                'git_list': git_list,
                'parent': parent,
                'base': base,
                'extra': extra,
            }
        )
    return HttpResponse(template.render(context))

def new_repo(request):
    print 'new_repo'
    if request.method == 'POST':
        form = NewRepo(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('')
    else:
        form = NewRepo()
        template = loader.get_template('lister/new_repo.html')
        return HttpResponse(template.render(context))

