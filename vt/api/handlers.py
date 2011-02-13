from piston.handler import BaseHandler
from piston.utils import rc
from vt.valentunes.models import CardModel
from vt.valentunes.forms import CardModelForm

class CardHandler(BaseHandler):
    allowed_methods = ('POST', 'GET', 'DELETE',)
    
    # def create(self, request):
    #     import pdb; pdb.set_trace()
    #     f = CardModelForm(request.POST)
    #     if f.is_valid():
    #         new_object = f.save()
    #         return new_object
    #     else:
    #         import pdb; pdb.set_trace()
    #         return rc.BAD_REQUEST

    def create(self, request):
           print request
           if request.content_type:
               data = request.data
               print data
               import pdb; pdb.set_trace;
               em = self.model(from_name=data['from_name'], to_name=data['to_name'], interests=data['interests'])
               em.save()
    
               # for comment in data['comments']:
               #     Comment(parent=em, content=comment['content']).save()
    
               return rc.CREATED
           else:
               print "Problem creating record."
           # else:
           #     super(ExpressiveTestModel, self).create(request)

    def read(self, request, object_id):
        card_object = CardModel.objects.get(id=object_id)
        return card_object
        
    def delete(self, request, object_id):
        card_object = CardModel.objects.get(id=object_id)
        card_object.delete()
        return rc.DELETED