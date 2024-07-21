from django import forms
from .operations import Vente, VenteItem,Remboursement,Charge
from .models import Poule,Oeuf,ChargeCategory

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['date_vente','client', 'remise','montant_dette']
        widgets = {
            'date_vente': forms.DateInput(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'remise': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'montant_dette': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class VenteItemForm(forms.ModelForm):
    class Meta:
        model = VenteItem
        fields = ['produit_poule', 'produit_oeuf', 'quantite']
        widgets = {
            'produit_poule': forms.Select(attrs={'class': 'form-control'}),
            'produit_oeuf': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }



class RemboursementForm(forms.ModelForm):
    class Meta:
        model = Remboursement
        fields = ['vente', 'montant', 'remarque']
        widgets = {
            'vente': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remarque': forms.Textarea(attrs={'class': 'form-control'}),
        }




class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = ['category', 'fournisseur', 'description', 'montant', 'montant_paye']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'montant_paye': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }



class PouleForm(forms.ModelForm):
    class Meta:
        model = Poule
        fields = ['race', 'description', 'prix_unitaire', 'photo']
        widgets = {
            'race': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class OeufForm(forms.ModelForm):
    class Meta:
        model = Oeuf
        fields = ['nom', 'description', 'prix_unitaire', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ChargeCategoryForm(forms.ModelForm):
    class Meta:
        model = ChargeCategory
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }