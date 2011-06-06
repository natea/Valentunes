from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.serializers import Serializer
from tastypie import fields
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys, trailing_slash
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError, ImmediateHttpResponse
from django.http import HttpResponse, HttpResponseNotFound

from valentunes.models import Card, Track
import simplejson as json

from time import sleep

        
class TrackResource(ModelResource):
    class Meta:
        queryset = Track.objects.all()
        resource_name = 'track'
        authorization = Authorization()
        # card = fields.ForeignKey(CardResource, 'card')
        
        
class CardResource(ModelResource):
    track_set = fields.ToManyField(TrackResource, 'track_set', full=True)

    class PerUserAuthentication(BasicAuthentication):
        def apply_limits(self, request, object_list):
            if request and hasattr(request, 'GET') and request.GET.get('user'):
                if request.GET['user'].is_authenticated():
                    object_list = object_list.filter(user=request.GET['user'])
                else:
                    object_list = object_list.none()

            return object_list

    class Meta:
        queryset = Card.objects.all()
        resource_name = 'card'
        authentication = PerUserAuthentication()
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
        
    def is_authenticated(self, request):
        """
        Handles checking if the user is authenticated and dealing with
        unauthenticated users.

        Mostly a hook, this uses class assigned to ``authentication`` from
        ``Resource._meta``.
        """
        # Authenticate the request as needed.
        auth_result = self._meta.authentication.is_authenticated(request)

        if isinstance(auth_result, HttpResponse):
            raise ImmediateHttpResponse(response=auth_result)

        if not auth_result is True:
            raise ImmediateHttpResponse(response=json.dump({'code': '115', 'message': 'Bad username or password.'}))
