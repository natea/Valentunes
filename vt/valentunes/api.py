from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.serializers import Serializer
from tastypie import fields
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys, trailing_slash
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError, ImmediateHttpResponse, ApiFieldError
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings

from valentunes.models import Card, Track
import simplejson as json

from time import sleep

# If ``csrf_exempt`` isn't present, stub it.
try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    def csrf_exempt(func):
        return func

def json_response(x):
    return HttpResponse(json.dumps(x, sort_keys=True, indent=2),
                        content_type='application/json; charset=UTF-8')
        
class TrackResource(ModelResource):
    class Meta:
        queryset = Track.objects.all()
        resource_name = 'track'
        authorization = Authorization()
        # card = fields.ForeignKey(CardResource, 'card')
        
class CardResource(ModelResource):
    track_set = fields.ToManyField(TrackResource, 'track_set', full=True)

    def get_object_list(self, request, *args, **kwargs):
        return Card.objects.filter(user=request.user)
                  
    # overriding wrap_view to ensure that errors are returned as JSON rather than HTML
    # and that we have sensible error messages returned to the user for situations
    # where the user has entered an incorrect username or password.
    def wrap_view(self, view):
        """
        Wraps methods so they can be called in a more functional way as well
        as handling exceptions better.

        Note that if ``BadRequest`` or an exception with a ``response`` attr
        are seen, there is special handling to either present a message back
        to the user or return the response traveling with the exception.
        """
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            try:
                callback = getattr(self, view)
                response = callback(request, *args, **kwargs)


                if request.is_ajax():
                    # IE excessively caches XMLHttpRequests, so we're disabling
                    # the browser cache here.
                    # See http://www.enhanceie.com/ie/bugs.asp for details.
                    patch_cache_control(response, no_cache=True)

                return response
            except (BadRequest, ApiFieldError), e:
                return HttpBadRequest(e.args[0])
            except ValidationError, e:
                return HttpBadRequest(', '.join(e.messages))
            except Exception, e:
                if hasattr(e, 'response'):
                    # 401 is the HTTP status code for Unauthorized, so we explicitly inform the user of this error.
                    if e.response.status_code == 401:
                        return json_response({ 'code' : '1',
                                               'message' : 'Bad username or password.'})
                    else:
                        message = ', '.join(e.messages)
                        return json_response({ 'code': '2',
                                               'message' : message })
                                               
                # A real, non-expected exception.
                # Handle the case where the full traceback is more helpful
                # than the serialized error.
                if settings.DEBUG and getattr(settings, 'TASTYPIE_FULL_DEBUG', False):
                    raise

                # Rather than re-raising, we're going to things similar to
                # what Django does. The difference is returning a serialized
                # error message.
                return self._handle_500(request, e)

        return wrapper

    def json_response(x):
            import json
            return HttpResponse(json.dumps(x, sort_keys=True, indent=2),
                                content_type='application/json; charset=UTF-8')

    class Meta:
        queryset = Card.objects.all()
        resource_name = 'card'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
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

        updated_bundle = self.obj_create(bundle, request=request, user=request.user)

        updated_bundle.obj.get_tracks()
#        updated_bundle.obj.get_track_urls()

        # return self.create_response(request, {'id': updated_bundle.obj.id, "track_list": track_list })
        return self.create_response(request, self.full_dehydrate(bundle.obj))