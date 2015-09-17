from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from .models import Entry
import os
import os.path

def index(request):
    #entry_list = Entry.objects.all()
    entry_list = []
    parent = request.path
    start = '.' + parent
    for p, d, f in os.walk(start):
        entry_list = [Entry(path=p) for p in d]
        d[:] = []
    template = loader.get_template('lister/index.html')
    context = RequestContext(request,
            {
                'entry_list': entry_list,
                'parent': parent,
            }
        )
    return HttpResponse(template.render(context))

