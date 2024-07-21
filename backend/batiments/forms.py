from django import forms
from .models import Batiment

class BatimentForm(forms.ModelForm):
    class Meta:
        model = Batiment
        fields = ['nom', 'description', 'capacite', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du bâtiment'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description du bâtiment',
                'rows': 4
            }),
            'capacite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Capacité du bâtiment'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }