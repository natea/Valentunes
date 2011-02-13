from django.db import models

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
    
    def __unicode__(self):
        return u"CardModel"

    @models.permalink
    def get_absolute_url(self):
        return ('CardModel', [self.id])
    
class TrackModel(models.Model):
    """ Track is a song that we've found on MusixMatch based on
    the recipients' interests.
    """
#    cards = models.ManyToManyField(CardModel, related_name="track_card_set")
    card = models.ForeignKey(CardModel)
    track_id = models.IntegerField(),
    track_mbid = models.CharField(max_length=50),
    lyrics_id = models.IntegerField(),
    subtitle_id = models.IntegerField(),
    track_name = models.CharField(max_length=100),
    artist_id = models.IntegerField(),
    album_coverart_100x100 = models.URLField(max_length=200)
    # example URL of album_coverart: http:\/\/api.musixmatch.com\/albumcover\/741317.jpg",
    artist_mbid = models.CharField(max_length=200)

    def __unicode__(self):
        return u"TrackModel"

    @models.permalink
    def get_absolute_url(self):
        return ('TrackModel', [self.id])
    