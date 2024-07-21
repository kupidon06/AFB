# forms.py
from django import forms
from batiments.models import Batiment
from .models import Race, Lot, Aliment, Traitement
from .rapport import JournalisationQuotidienne, Alimentation, RamassageOeufs, HistoriqueTraitement, Provision

class RaceForm(forms.ModelForm):
    nom = forms.CharField(
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
    )
    photo = forms.ImageField(
        label="Photo",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Race
        fields = ['nom', 'description', 'photo']

class BandeForm(forms.ModelForm):
    nom = forms.CharField(
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    race = forms.ModelChoiceField(
        queryset=Race.objects.all(),
        label="Race",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    batiment = forms.ModelChoiceField(
        queryset=Batiment.objects.all(),
        label="Bâtiment",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_arrivee = forms.DateField(
        label="Date d'arrivée",
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date d\'arrivée', 'type': 'date'})
    )
    age_arrivee = forms.IntegerField(
        label="Âge à l'arrivée",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Âge à l\'arrivée'})
    )
    nombre_arrivee = forms.IntegerField(
        label="Nombre à l'arrivée",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre à l\'arrivée'})
    )

    nombre_deces = forms.IntegerField(
        label="Nombre de décès",
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de décès'})
    )
    nombre_malade = forms.IntegerField(
        label="Nombre de malades",
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de malades'})
    )
    traitement_imminent = forms.IntegerField(
        label="Traitement imminent",
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Traitement imminent'})
    )
    details = forms.CharField(
        label="Détails",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Détails'})
    )

    class Meta:
        model = Lot
        fields = [
            'nom', 'race', 'batiment', 'date_arrivee', 'age_arrivee',
            'nombre_arrivee', 'nombre_deces',
            'nombre_malade', 'traitement_imminent', 'details'
        ]

class BandeUpdateForm(forms.ModelForm):
    nom = forms.CharField(
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    race = forms.ModelChoiceField(
        queryset=Race.objects.all(),
        label="Race",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    batiment = forms.ModelChoiceField(
        queryset=Batiment.objects.all(),
        label="Bâtiment",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_arrivee = forms.DateField(
        label="Date d'arrivée",
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    age_arrivee = forms.IntegerField(
        label="Âge à l'arrivée",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Âge à l\'arrivée'})
    )
    nombre_arrivee = forms.IntegerField(
        label="Nombre à l'arrivée",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre à l\'arrivée'})
    )

    nombre_deces = forms.IntegerField(
        label="Nombre de décès",
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de décès'})
    )
    nombre_malade = forms.IntegerField(
        label="Nombre de malades",
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de malades'})
    )
    traitement_imminent = forms.IntegerField(
        label="Traitement imminent",
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Traitement imminent'})
    )
    details = forms.CharField(
        label="Détails",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Détails'})
    )

    class Meta:
        model = Lot
        fields = [
            'nom', 'race', 'batiment', 'date_arrivee', 'age_arrivee',
            'nombre_arrivee', 'nombre_deces',
            'nombre_malade', 'traitement_imminent', 'details'
        ]


class AlimentForm(forms.ModelForm):
    UNITE_CHOICES = (
        ('kg', 'Kilogrammes'),
        ('g', 'Grammes'),
        ('L', 'Litres'),
        ('ml', 'Millilitres'),
        ('unité', 'Unité'),
    )

    nom = forms.CharField(
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
    )
    prix_unitaire = forms.DecimalField(
        label="Prix unitaire",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix unitaire'})
    )
    unite_mesure = forms.ChoiceField(
        label="Unité de mesure",
        choices=UNITE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Aliment
        fields = ['nom', 'description', 'prix_unitaire', 'unite_mesure']

class TraitementForm(forms.ModelForm):
    nom = forms.CharField(
        label="Nom",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'})
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'})
    )
    duree_jours = forms.IntegerField(
        label="Durée (jours)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Durée (jours)'})
    )

    class Meta:
        model = Traitement
        fields = ['nom', 'description', 'duree_jours']
#-------------------------------------operations---------------------------------------------------------------------
class JournalisationQuotidienneForm(forms.ModelForm):
    class Meta:
        model = JournalisationQuotidienne
        exclude = ['lot']  # Exclure le champ lot des champs affichés

    def __init__(self, *args, **kwargs):
        lot_id = kwargs.pop('lot_id', None)  # Récupérer lot_id depuis les arguments kwargs
        super().__init__(*args, **kwargs)
        if lot_id:
            self.instance.lot_id = lot_id  # Assigner lot_id à l'instance du formulaire
        self.fields['date_journalisation'].widget.attrs.update({
            'class': 'form-control',  # Ajout de la classe form-control
            'type': 'date'  # Définition du type de champ à date
        })
        self.fields['nombre_vivants'].widget.attrs['class'] = 'form-control'
        self.fields['nombre_deces'].widget.attrs['class'] = 'form-control'
        self.fields['nombre_malades'].widget.attrs['class'] = 'form-control'
        self.fields['autres_informations'].widget.attrs['class'] = 'form-control'


class AlimentationForm(forms.ModelForm):
    class Meta:
        model = Alimentation
        exclude = ['lot']

    def __init__(self, *args, **kwargs):
        lot_id = kwargs.pop('lot_id', None)
        super().__init__(*args, **kwargs)
        if lot_id:
            self.instance.lot_id = lot_id
        self.fields['date_alimentation'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Sélectionnez une date',
        })
        self.fields['quantite'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Entrez la quantité (kg)',
        })
        self.fields['type_aliment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Entrez le type d\'aliment',
        })
        self.fields['commentaire'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Entrez un commentaire (optionnel)',
        })


class RamassageOeufsForm(forms.ModelForm):
    class Meta:
        model = RamassageOeufs
        exclude = ['lot']  # Exclure le champ lot des champs affichés

    def __init__(self, *args, **kwargs):
        lot_id = kwargs.pop('lot_id', None)  # Récupérer lot_id depuis les arguments kwargs
        super().__init__(*args, **kwargs)
        if lot_id:
            self.instance.lot_id = lot_id  # Assigner lot_id à l'instance du formulaire
        self.fields['date_ramassage'].widget.attrs['class'] = 'form-control'
        self.fields['date_ramassage'].widget.attrs['type'] = 'date'
        self.fields['quantite_premier_ramassage'].widget.attrs['class'] = 'form-control'
        self.fields['quantite_deuxieme_ramassage'].widget.attrs['class'] = 'form-control'
        self.fields['quantite_troisieme_ramassage'].widget.attrs['class'] = 'form-control'
        self.fields['quantite_quatrieme_ramassage'].widget.attrs['class'] = 'form-control'
        self.fields['commentaire'].widget.attrs['class'] = 'form-control'

class HistoriqueTraitementForm(forms.ModelForm):
    class Meta:
        model = HistoriqueTraitement
        exclude = ['lot']  # Exclure le champ lot des champs affichés

    def __init__(self, *args, **kwargs):
        lot_id = kwargs.pop('lot_id', None)  # Récupérer lot_id depuis les arguments kwargs
        super().__init__(*args, **kwargs)

        # Initialisation de lot_id s'il est passé en argument
        if lot_id:
            self.instance.lot_id = lot_id
        self.fields['date_traitement'].widget.attrs.update({
            'class': 'form-control',  # Ajout de la classe form-control
            'type': 'date'  # Définition du type de champ à date
        })

        # Définition des classes CSS pour chaque champ
        self.fields['traitement'].widget.attrs['class'] = 'form-control'
          # Utilisation du type date pour le champ date_traitement
        self.fields['commentaire'].widget.attrs['class'] = 'form-control'

class ProvisionForm(forms.ModelForm):
    class Meta:
        model = Provision
        fields = ['fournisseur', 'aliment', 'quantite', 'date_provision']
        widgets = {
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
            'aliment': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_provision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_date_provision(self):
        date_provision = self.cleaned_data.get('date_provision')
        print(f"Cleaned Date: {date_provision}")
        return date_provision


class ProvisionUpdateForm(forms.ModelForm):
    class Meta:
        model = Provision
        fields = ['fournisseur', 'aliment', 'quantite', 'date_provision']
        widgets = {
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
            'aliment': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_provision': forms.DateInput(attrs={'class': 'form-control'}),
        }

