from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from .models import Entry
import os
import os.path

def index(request):
    #entry_list = Entry.objects.all()
    entry_list = []
    base = request.path
    if base.endswith('/'):
        parent = ''
    else:
        if base.count('/') > 1:
            parent = base[:base.rfind('/')]
        else:
            parent = '/'
        base = base + '/'
    for path, dirs, files in os.walk('.' + base):
        entry_list = [Entry(path=d) for d in dirs if not d.startswith('.')]
        break
    print 'base', base
    print 'parent', parent
    template = loader.get_template('lister/index.html')
    context = RequestContext(request,
            {
                'entry_list': entry_list,
                'parent': parent,
                'base': base,
            }
        )
    return HttpResponse(template.render(context))

