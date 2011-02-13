from django import forms
from models import CardModel,TrackModel

class CardModelForm(forms.ModelForm):
    class Meta:
        model = CardModel

from django.forms.models import modelformset_factory

TrackModelFormSet = modelformset_factory(TrackModel)
