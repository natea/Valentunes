from django.db import models
import urllib
import json

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
        return u"CardModel"

    @models.permalink
    def get_absolute_url(self):
        return ('CardModel', [self.id])
    
    def get_tracks(self):
        #get lyrics that mention to_name
        mkey='b6b0c3fb765dd2368d6f309f23448982'
        lyr_url = "http://api.musixmatch.com/ws/1.1/track.search"
        params=urllib.urlencode({'apikey':mkey,'q_lyrics':self.to_name,'format':'json'})
        #make the url call
        f=urllib.urlopen(lyr_url,params)
        j=json.load(f)
        #check that j has a 200 and is good
        #iterate over these tracks and add them to an array of tracks we've found, adding in the search term
        for track in j['message']['body']['track_list']:
            track = track['track']
            t = TrackModel(card=self,track_name=track['track_name'],artist_name=track['artist_name'],track_mbid=track['track_mbid'],artist_mbid=track['artist_mbid'],album_coverart_100x100=track['album_coverart_100x100'])
            #t = TrackModel(card=self)
            #t.track_name=track['track_name']
            t.save()

        #TODO: repeat this for the notes

    def get_track_urls(self):
        #so now that we've got all these tracks, let's get urls for them.
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
    
