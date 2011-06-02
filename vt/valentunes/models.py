from django.db import models
import urllib
import json
import httplib2
#TODO make this in a better place
from BeautifulSoup import BeautifulStoneSoup

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.conf import settings

class Card(models.Model):
    """ Card is a valentine's day card that contains the information
    about who the card is from and who it's to, what the recipients
    interests are and a personal note.
    """
    user = models.ForeignKey(User)
    recipient_name = models.CharField(max_length=200, blank=True)
    recipient_email = models.EmailField(max_length=200, null=True, blank=True)
    recipient_phone = models.CharField(max_length=200, blank=True)
    intro_note = models.TextField(max_length=1000, blank=True)
    interests = models.TextField(max_length=1000, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    class Admin:
        pass

    def __unicode__(self):
        return u"%s"%("Card"+str(self.id)+" from "  + " to " + self.recipient_name)
        
    @models.permalink
    def get_absolute_url(self):
        return ('Card', [self.id])
      
    def get_topic_tracks(self,topic):
        """Given a topic, find all the tracks that have lyrics matching that topic"""
        
        lyr_url = "http://api.musixmatch.com/ws/1.1/track.search"
        try:
            params = urllib.urlencode({'apikey':settings.MUSIXMATCH_KEY,'q_lyrics':topic,'format':'json'})
            f = urllib.urlopen(lyr_url,params)
        except: 
            #if we can't get this, there is no point
            return
        #make the url call
        j=json.load(f)
#        print j['message']['body']['track_list']
#        import pdb; pdb.set_trace()

        #TODO check that j has a 200 and is good
        #iterate over these tracks and add them to an array of tracks we've found, adding in the search term
        for track in j['message']['body']['track_list']:
            track = track['track']
            print track
            print self
            t = Track(track_name=track['track_name'],artist_name=track['artist_name'],track_mbid=track['track_mbid'],artist_mbid=track['artist_mbid'],search_term=topic,album_coverart_100x100=track['album_coverart_100x100'])
            print t
            t.save()
            t.card.add(self)
            t.save()
        
    def get_tracks(self):
        """Get tracks that have the person's name in the lyrics or have their interests in the lyrics"""
        
        self.get_topic_tracks(self.recipient_name)

        #TODO: repeat this for the notes
        interests_list = self.interests.split(',')
        for topic in interests_list:
            self.get_topic_tracks(topic)


    def get_track_urls(self):
        """For each track, get the URL for it"""
    
        track_bucket = Track.objects.filter(card=self.id)
        if track_bucket:
            for track in track_bucket:
                track.get_audio_url()

    
class Track(models.Model):
    """ Track is a song that we've found on MusixMatch based on the recipients' interests."""
    
    card = models.ManyToManyField(Card, related_name="track_card_set")
#    card = models.ForeignKey(CardModel)
    track_mbid = models.CharField(max_length=50)
    track_name = models.CharField(max_length=200)
    album_coverart_100x100 = models.URLField(max_length=200)
    # example URL of album_coverart: http:\/\/api.musixmatch.com\/albumcover\/741317.jpg",
    artist_name = models.CharField(max_length=200)
    artist_mbid = models.CharField(max_length=200)
    audio_url = models.URLField(max_length=640)
    search_term = models.CharField(max_length=200)
    #should we remove this track from the card?
    remove = models.BooleanField(default=True)

    class Admin:
        pass

    def __unicode__(self):
        return u"%s"%(self.artist_name+" - " + self.track_name)

    @models.permalink
    def get_absolute_url(self):
        return ('Track', [self.id])


    def get_audio_url(self):
        """TODO: Replace this with Echonest+Rdio since Skreemr's API is currently unavailable:
        http://skreemr.com/licensing.jsp"""
        
        skr_url = 'http://skreemr.com/skreemr-web-service/search'
        try:
            params=urllib.urlencode({'song':self.track_name,'artist':self.artist_name,})
            f = urllib.urlopen(skr_url+'?'+params)
        except:
            #what can we do with this?  get rid of it
            self.delete()
            return

        soup = BeautifulStoneSoup(f.read())
        urls = soup.findAll('url')
        for url in urls:
            url = url.string
            if self.verify_url(url):
              self.audio_url = url
              self.save()
              return
        #we can't find audio for this - useless!
        self.delete()
        return


    def verify_url(self,iffy_url):
        """Check to make sure that the URL exists
        TODO: check that the mime type is an MP3 file
        """
        
        validate = URLValidator(verify_exists=True)
        try:
            result = validate(iffy_url)
            if result is None:
                return True
        except ValidationError, e:
            print e
            return False

class UserProfile(models.Model):  
    """User profile lets us collect name, email and phone info.
    as per http://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django"""
    
    user = models.OneToOneField(User)  
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=75, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self):  
          return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)     