from django.contrib import admin
from valentunes.models import TrackModel,CardModel
class TrackAdmin(admin.ModelAdmin):
    pass
admin.site.register(TrackModel,TrackAdmin)
admin.site.register(CardModel)
