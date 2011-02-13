from django.db import models
import urllib
import json
import httplib2
#TODO make this in a better place
from BeautifulSoup import BeautifulStoneSoup

# Create your models here.

class CardModel(models.Model):
    """ Card is a valentine's day card that contains the information
    about who the card is from and who it's to, what the recipients
    interests are and a personal note.
    """
    from_name = models.CharField(max_length=200)
    from_email = models.EmailField(max_length=75)
    from_phone = models.CharField(max_length=50, blank=True)
    to_name = models.CharField(max_length=200, blank=True)
    to_email = models.EmailField(max_length=200, blank=True)
    to_phone = models.CharField(max_length=200, blank=True)
    intro_note = models.TextField(max_length=1000, blank=True)
    interests = models.TextField(max_length=1000, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    class Admin:
        pass

    def __unicode__(self):
        return u"%s"%("Card"+str(self.id)+" from " + self.from_name + " to " + self.to_name)

    @models.permalink
    def get_absolute_url(self):
        return ('CardModel', [self.id])
      
    def get_topic_tracks(self,topic):
        mkey='b6b0c3fb765dd2368d6f309f23448982'
        lyr_url = "http://api.musixmatch.com/ws/1.1/track.search"
        try:
            params=urllib.urlencode({'apikey':mkey,'q_lyrics':topic,'format':'json'})
            f=urllib.urlopen(lyr_url,params)
        except: 
            #if we can't get this, there is no point
            return;
        #make the url call
        j=json.load(f)
        #check that j has a 200 and is good
        #iterate over these tracks and add them to an array of tracks we've found, adding in the search term
        for track in j['message']['body']['track_list']:
            track = track['track']
            t = TrackModel(card=self,track_name=track['track_name'],artist_name=track['artist_name'],track_mbid=track['track_mbid'],artist_mbid=track['artist_mbid'],reason=topic,album_coverart_100x100=track['album_coverart_100x100'])
            t.save()
        
    def get_tracks(self):
        #get lyrics that mention to_name
        self.get_topic_tracks(self.to_name)

        #TODO: repeat this for the notes
        interests_list = self.interests.split(',')
        for topic in interests_list:
          self.get_topic_tracks(topic)


    def get_track_urls(self):
        #so now that we've got all these tracks, let's get urls for them.
        my_track_bucket=TrackModel.objects.filter(card=self.id)
        for track in my_track_bucket:
            track.get_audio_url()
            


        return 4
        
        

        
      


    
class TrackModel(models.Model):
    """ Track is a song that we've found on MusixMatch based on
    the recipients' interests.
    """
#    cards = models.ManyToManyField(CardModel, related_name="track_card_set")
    card = models.ForeignKey(CardModel)
    track_mbid = models.CharField(max_length=50)
    track_name = models.CharField(max_length=200)
    album_coverart_100x100 = models.URLField(max_length=200)
    # example URL of album_coverart: http:\/\/api.musixmatch.com\/albumcover\/741317.jpg",
    artist_name = models.CharField(max_length=200)
    artist_mbid = models.CharField(max_length=200)
    audio_url = models.URLField(max_length=640)
    reason = models.CharField(max_length=200)

    class Admin:
        pass

    def __unicode__(self):
        return u"%s"%(self.artist_name+" - " + self.track_name)

    @models.permalink
    def get_absolute_url(self):
        return ('TrackModel', [self.id])


    def get_audio_url(self):
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
        #I declare all urls to be good.
        #TODO actually check the urls
        h = httplib2.Http()
        resp = h.request(iffy_url, 'HEAD')
        return resp[0]['status']=='200'
