from django import forms
from .models import Opiniones

class OpinionesForm(forms.ModelForm):
    class Meta:
        model = Opiniones
        fields = ['asunto', 'opinion', 'puntuacion']