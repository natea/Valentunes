from django import forms
from models import CardModel

class CardModelForm(forms.ModelForm):
    class Meta:
        model = CardModel