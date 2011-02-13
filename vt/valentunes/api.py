from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.serializers import Serializer
from tastypie import fields
from valentunes.models import CardModel, TrackModel

class CardResource(ModelResource):
    class Meta:
        queryset = CardModel.objects.all()
        resource_name = 'card'
        authorization = Authorization()
        serializer = Serializer()
        
class TrackResource(ModelResource):
    class Meta:
        queryset = TrackModel.objects.all()
        resource_name = 'track'
        authorization = Authorization()
        card = fields.ForeignKey(CardResource, 'card')