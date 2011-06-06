from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer
from tastypie import fields
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys, trailing_slash
from valentunes.models import Card, Track



from time import sleep

        
class TrackResource(ModelResource):
    class Meta:
        queryset = Track.objects.all()
        resource_name = 'track'
        authorization = Authorization()
        # card = fields.ForeignKey(CardResource, 'card')
        
        
class CardResource(ModelResource):
    track_set = fields.ToManyField(TrackResource, 'track_set', full=True)

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

        updated_bundle.obj.get_tracks()
#        updated_bundle.obj.get_track_urls()

        # return self.create_response(request, {'id': updated_bundle.obj.id, "track_list": track_list })
        return self.create_response(request, self.full_dehydrate(bundle.obj))