from piston.handler import BaseHandler
from piston.utils import rc
from vt.valentunes.models import CardModel
from vt.valentunes.forms import CardModelForm

class CardHandler(BaseHandler):
    allowed_methods = ('POST', 'GET', 'DELETE',)
    
    def create(self, request):
        f = CardModelForm(request.POST)
        if f.is_valid():
            new_object = f.save()
            if new_object.to_name != "":
                new_object.get_tracks()
            return new_object
        return rc.BAD_REQUEST
        
    def read(self, request, object_id):
        card_object = CardModel.objects.get(id=object_id)
        return card_object
        
    def delete(self, request, object_id):
        card_object = CardModel.objects.get(id=object_id)
        card_object.delete()
        return rc.DELETED
