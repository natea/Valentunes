# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django import forms
from models import TrackModel, CardModel
from vt.valentunes.forms import CardModelForm

def index(request,template_name='index.html'):
    if request.method == 'POST':
        #handle the poste
        form = CardModelForm(request.POST)
        if form.is_valid():
            #handle the form, insert stuff
            new_object = form.save()
            if new_object.to_name != "":
                new_object.get_tracks()
                new_object.get_track_urls()
            return HttpResponseRedirect('/choose/%s/'%new_object.id) 
    else:
        form = CardModelForm()
    context = {'form':form}
    return render_to_response(template_name, context,context_instance=RequestContext(request))

def choose(request, cardid, template_name='choose.html'):
    track_list = TrackModel.objects.filter(card=cardid)

    context = {'track_list':track_list}
    return render_to_response(template_name, context,context_instance=RequestContext(request))

