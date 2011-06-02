from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer
from tastypie import fields
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys, trailing_slash
from valentunes.models import Card, Track

from time import sleep

class CardResource(ModelResource):
    class Meta:
        queryset = Card.objects.all()
        resource_name = 'card'
        authorization = Authorization()
        serializer = Serializer()
        
    def post_list(self, request, **kwargs):
        """
        Creates a new resource/object with the provided data.

        Calls ``obj_create`` with the provided data and returns a response
        with the new resource's location.

        If a new resource is created, return ``HttpCreated`` (201 Created).
        """
        deserialized = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT_TYPE', 'application/json'))
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized))
        self.is_valid(bundle, request)
        updated_bundle = self.obj_create(bundle, request=request)
        cardid = updated_bundle.obj.id
        tracks = None

        updated_bundle.obj.get_tracks()
#        updated_bundle.obj.get_track_urls()
    
        while not tracks:
            tracks = Track.objects.filter(card=cardid)
            print "Waiting"
            sleep(1)

        track_list = []
                    
        for track in tracks:
            d = {} 
            d['track_id'] = track.id
            d['track_mbid'] = track.track_mbid
            d['track_name'] = track.track_name
            d['search_term'] = track.search_term
            d['audio_url'] = track.audio_url
            d['icon_url'] = track.album_coverart_100x100
            d['artist_name'] = track.artist_name
            #import pdb; pdb.set_trace()
            track_list.append(d)
            
        return self.create_response(request, {'id': updated_bundle.obj.id, "track_list": track_list })
        
class TrackResource(ModelResource):
    class Meta:
        queryset = Track.objects.all()
        resource_name = 'track'
        authorization = Authorization()
        card = fields.ForeignKey(CardResource, 'card')