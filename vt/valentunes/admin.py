from django.contrib import admin
from valentunes.models import Track, Card, UserProfile

class TrackAdmin(admin.ModelAdmin):
    pass
    
class CardAdmin(admin.ModelAdmin):
    pass

admin.site.register(Track,TrackAdmin)
admin.site.register(Card)
admin.site.register(UserProfile)