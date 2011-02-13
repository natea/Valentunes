# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import TrackModel, CardModel

def index(request,template_name='index.html'):
    context = {}
    return render_to_response(template_name, context,context_instance=RequestContext(request))

def choose(request, cardid, template_name='choose.html'):
    track_list = TrackModel.objects.filter(card=cardid)

    context = {'track_list':track_list}
    return render_to_response(template_name, context,context_instance=RequestContext(request))

