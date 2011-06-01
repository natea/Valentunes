from django import forms
from models import Card, Track

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        exclude = ('user',)

from django.forms.models import modelformset_factory

TrackFormSet = modelformset_factory(Track)
