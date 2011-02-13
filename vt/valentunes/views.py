# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request,template_name='index.html'):
    context = {}
    return render_to_response(template_name, context,context_instance=RequestContext(request))

