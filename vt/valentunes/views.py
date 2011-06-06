# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from models import Track, Card
from django.http import HttpResponseRedirect, HttpResponse
from vt.valentunes.forms import CardForm, TrackFormSet
import urllib


@login_required
def index(request, template_name='index.html'):
    if request.method == 'POST':
        #handle the post
        form = CardForm(request.POST)
        if form.is_valid():
            #handle the form, insert stuff
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            # make sure the recipient's name is not blank
            if card.recipient_name != "":
                card.get_tracks()
                card.get_track_urls()
            return HttpResponseRedirect('/choose/%s/' % card.id) 
    else:
        form = CardForm()
    context = {'form':form}
    return render_to_response(template_name, context,context_instance=RequestContext(request))

def gift(request, cardid, template_name='gift.html'):
    card = Card.objects.get(id__exact=cardid)
    track_list = Track.objects.filter(card=cardid)
    context = {'track_list':track_list, 'card':card}
    return  render_to_response(template_name, context,context_instance=RequestContext(request))

def playlist(request,cardid,template_name='playlist.xml'):
    card = Card.objects.filter(id=cardid)
    track_list = Track.objects.filter(card=cardid)
    context = {'track_list':track_list, 'card':card}
    return  render_to_response(template_name, context,context_instance=RequestContext(request))

def choose(request, cardid, template_name='choose.html'):
    if request.method == 'POST':
        #handle the post
        objs = request.POST
        trackids = objs.getlist('track')
        songstext = ""
        tracks = Track.objects.filter(card=cardid)
        for trackid in trackids:
            track = tracks.get(id__exact=trackid)
            songstext +='{"title":"'+track.track_name+'","url":"'+track.audio_url+'"},'
            track.remove = False
            track.save()
          
        tracks.filter(remove=True).delete()
          
        if objs.get('phone_call') == 'Send a Phone Call':
            #post to the phone 
            card = Card.objects.get(id__exact=cardid)
            jstr = '{"to":"'+card.recipient_name+'","from":"'+card.user.get_profile().name + '","phone":"'+card.recipient_phone+'","message":"'+card.intro_note+'","songs":['+songstext[:-1]+']}'
            print jstr
            args = {}
            args['data'] = jstr;
            args_enc = urllib.urlencode(args)
            res = urllib.urlopen('http://seevl.net/tmp/valentunes/cgi.py/call', args_enc).read()
            #done!

            return render_to_response("sent.html", { 
                  "recipient_name": card.recipient_name,
                  "to_phone": card.recipient_phone,
                  },
                                    RequestContext(request))
        else:
            #post to the gifts
            return HttpResponseRedirect('/gift/%s/'%cardid)
            
    else:
        form = TrackFormSet(queryset=Track.objects.filter(card=cardid))
        track_list = Track.objects.filter(card=cardid)
        context = {'track_list':track_list,'formset':form}
        return render_to_response(template_name, context,context_instance=RequestContext(request))

