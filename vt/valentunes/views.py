# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django import forms
from models import TrackModel, CardModel
from django.http import HttpResponseRedirect, HttpResponse
from vt.valentunes.forms import CardModelForm, TrackModelFormSet
import urllib

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
    if request.method == 'POST':
        #handle the post
        objs = request.POST
        print objs
        if objs.get('phone_call') == 'Phone Call':
          trackids=objs.getlist('track')
          print trackids
          songstext = ""
          tracks = TrackModel.objects.filter(card=cardid)
          for trackid in trackids:
            print trackid
            track = tracks.get(id__exact=trackid)
            songstext +='{"title":"'+track.track_name+'","url":"'+track.audio_url+'"},'
            print track.track_name
            track.remove =False
            

          tracks.filter(remove=True).delete()
          card = CardModel.objects.get(id__exact=cardid)
          
          #post to the phone 
          jstr = '{"to":"'+card.to_name+'","from":"'+card.from_name + '","phone":"'+card.to_phone+'","message":"'+card.intro_note+'","songs":['+songstext[:-1]+']}'
          print jstr
          args = {}
          args['data'] = jstr;
          args_enc = urllib.urlencode(args)
          #res = urllib.urlopen('http://seevl.net/tmp/valentunes/cgi.py/call', args_enc).read()
          #done!

          return render_to_response("sent.html", { 
                  "to_name": card.to_name,
                  "to_phone": card.to_phone,
                  },
                                    RequestContext(request))

        else:
          #post to the gifts
          return HttpResponseRedirect('/gift/%s/'%cardid)
    else:
        form = TrackModelFormSet(queryset=TrackModel.objects.filter(card=cardid))
        track_list = TrackModel.objects.filter(card=cardid)
        context = {'track_list':track_list,'formset':form}
        return render_to_response(template_name, context,context_instance=RequestContext(request))

