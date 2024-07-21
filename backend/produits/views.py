from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.http import HttpResponseRedirect,JsonResponse
from django.db.models import Sum
from django.contrib import messages
from django.views.decorators.http import require_http_methods,require_POST
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Race, Lot, Aliment, Traitement
from .rapport import JournalisationQuotidienne, Alimentation, RamassageOeufs, HistoriqueTraitement, Provision 
from .forms import (RaceForm, BandeForm, AlimentForm, TraitementForm,
JournalisationQuotidienneForm, AlimentationForm, RamassageOeufsForm,BandeUpdateForm,
 HistoriqueTraitementForm, ProvisionForm,ProvisionUpdateForm)



 #--------------------------------------------------operations----------------------------------------------------
 # JournalisationQuotidienne Views
# Views for JournalisationQuotidienne
@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def journalisation_quotidienne_list_view(request, lot_id=None):
    queryset = JournalisationQuotidienne.objects.all()
    query = request.GET.get('q')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    if lot_id:
        queryset = queryset.filter(lot_id=lot_id)

    if query:
        queryset = queryset.filter(
            Q(lot__nom__icontains=query) |
            Q(date_journalisation__icontains=query)
        )

    if date_min and date_max:
        queryset = queryset.filter(
            date_journalisation__gte=date_min,
            date_journalisation__lte=date_max
        )

    create_form = JournalisationQuotidienneForm(request.POST or None, lot_id=lot_id)
    
    if request.method == 'POST':
        create_form = JournalisationQuotidienneForm(request.POST, request.FILES, lot_id=lot_id)
        if create_form.is_valid():
                create_form.save()
                messages.success(request, 'Journalisation créée avec succès.')
                return redirect('journalisation-list', lot_id=lot_id)
        else:
                messages.error(request, 'Erreur lors de la création de la journalisation. Veuillez vérifier les données saisies.')
        

    context = {
        'journalisations': queryset,
        'create_form': create_form,
    }
    return render(request, 'journalisation/journalisation_list.html', context)

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def journalisation_quotidienne_update_view(request, pk):
    journalisation = get_object_or_404(JournalisationQuotidienne, pk=pk)
    form = JournalisationQuotidienneForm(request.POST or None, instance=journalisation)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('journalisation-list')  # Remplacez 'historique-traitement-list' par le nom correct de l'URL de la liste
        else:
            messages.error(request, 'Erreur lors de la mise à jour du traitement historique. Veuillez vérifier les données saisies.')

    context = {
        'form': form,
    }
    return render(request, 'journalisation/journalisation_form.html', context)


@login_required(login_url="/accounts/login/")
@require_http_methods(["POST"])
def journalisation_quotidienne_delete_view(request, pk):
    journalisation = get_object_or_404(JournalisationQuotidienne, pk=pk)
    lot_id = journalisation.lot_id
    journalisation.delete()
    messages.success(request, 'Journalisation supprimée avec succès.')
    return redirect('journalisation-list', lot_id=lot_id)

# Alimentation Views
@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def alimentation_list_view(request, lot_id=None):
    queryset = Alimentation.objects.filter(lot_id=lot_id) if lot_id else Alimentation.objects.all()

    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(lot__nom__icontains=query) |
            Q(date_alimentation__icontains=query)
        )

    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    if date_min and date_max:
        queryset = queryset.filter(
            date_alimentation__gte=date_min,
            date_alimentation__lte=date_max
        )

    create_form = AlimentationForm(request.POST or None, lot_id=lot_id)
    if create_form.is_valid():
        alimentation = create_form.save(commit=False)

        # Récupérer toutes les provisions pour l'aliment concerné
        total_provision = Provision.objects.filter(
            aliment=alimentation.type_aliment
        ).aggregate(total_quantite=Sum('quantite'))['total_quantite'] or 0

        # Calculer la somme des quantités utilisées dans les alimentations précédentes
        total_utilise = queryset.aggregate(total_quantite_utilisee=Sum('quantite'))['total_quantite_utilisee'] or 0

        # Comparer la quantité disponible avec la quantité utilisée
        if alimentation.quantite + total_utilise > total_provision:
            messages.error(request, 'La quantité demandée dépasse la quantité disponible en provision.')
        else:
            alimentation.save()
            messages.success(request, 'Alimentation créée avec succès.')
            return redirect('alimentation-list', lot_id=lot_id)
    else:
        messages.error(request, 'Erreur lors de la création de l\'alimentation. Veuillez vérifier les données saisies.')
    context = {
        'alimentations': queryset,
        'create_form': create_form,
    }
    return render(request, 'alimentation/alimentation_list.html', context)



from django.db.models import Sum

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def alimentation_update_view(request, pk):
    alimentation = get_object_or_404(Alimentation, pk=pk)

    if request.method == 'POST':
        form = AlimentationForm(request.POST, instance=alimentation)
        if form.is_valid():
            updated_alimentation = form.save(commit=False)

            # Récupérer toutes les provisions pour l'aliment spécifique
            provisions = Provision.objects.filter(aliment=updated_alimentation.type_aliment)
            total_provision = provisions.aggregate(total=Sum('quantite'))['total'] or 0

            # Récupérer toutes les alimentations existantes pour le même lot et le même aliment
            total_alimentation_utilisee = Alimentation.objects.filter(
                lot=updated_alimentation.lot,
                type_aliment=updated_alimentation.type_aliment
            ).exclude(pk=pk).aggregate(total=Sum('quantite'))['total'] or 0

            # Calculer la disponibilité totale
            total_disponible = total_provision - total_alimentation_utilisee

            # Vérifier la disponibilité
            if updated_alimentation.quantite > total_disponible:
                messages.error(request,
                               f"La quantité demandée ({updated_alimentation.quantite}) dépasse la quantité disponible ({total_disponible}).")
            else:
                updated_alimentation.save()
                messages.success(request, 'Alimentation mise à jour avec succès.')
                return redirect('alimentation-list')  # Remplacez 'alimentation-list' par le nom correct de l'URL de la liste
        else:
            messages.error(request,
                           'Erreur lors de la mise à jour de l\'alimentation. Veuillez vérifier les données saisies.')
    else:
        form = AlimentationForm(instance=alimentation)

    return render(request, 'alimentation/alimentation_form.html', {'form': form})



@login_required(login_url="/accounts/login/")
@require_http_methods(["POST"])
def alimentation_delete_view(request, pk):
    alimentation = get_object_or_404(Alimentation, pk=pk)
    lot_id = alimentation.lot_id
    alimentation.delete()
    messages.success(request, 'Alimentation supprimée avec succès.')
    return redirect('alimentation-list', lot_id=lot_id)


# RamassageOeufs Views
@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def ramassage_oeufs_list_view(request, lot_id=None):
    queryset = RamassageOeufs.objects.all()
    query = request.GET.get('q')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    if lot_id:
        queryset = queryset.filter(lot_id=lot_id)

    if query:
        queryset = queryset.filter(
            Q(lot__nom__icontains=query) |
            Q(date_ramassage__icontains=query)
        )

    if date_min and date_max:
        queryset = queryset.filter(
            date_ramassage__gte=date_min,
            date_ramassage__lte=date_max
        )

    create_form = RamassageOeufsForm(request.POST or None, lot_id=lot_id)

    if request.method == 'POST':
        create_form = RamassageOeufsForm(request.POST, request.FILES, lot_id=lot_id)
        if create_form.is_valid():
            create_form.save()
            messages.success(request, 'Ramassage d\'œufs créé avec succès.')
            return redirect('ramassage-list', lot_id=lot_id)
        else:
            messages.error(request, 'Erreur lors de la création du ramassage d\'œufs. Veuillez vérifier les données saisies.')

    context = {
        'ramassages': queryset,
        'create_form': create_form,
    }
    return render(request, 'ramassage/ramassage_list.html', context)



@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def ramassage_oeufs_update_view(request, pk):
    ramassage = get_object_or_404(RamassageOeufs, pk=pk)
    form = RamassageOeufsForm(request.POST or None, instance=ramassage)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('ramassage-list')  # Remplacez 'historique-traitement-list' par le nom correct de l'URL de la liste
        else:
            messages.error(request, 'Erreur lors de la mise à jour du traitement historique. Veuillez vérifier les données saisies.')

    context = {
        'form': form,
    }
    return render(request, 'ramassage/ramassage_form.html', context)


@login_required(login_url="/accounts/login/")
@require_POST
def ramassage_oeufs_delete_view(request, pk):
    ramassage = get_object_or_404(RamassageOeufs, pk=pk)
    lot_id = ramassage.lot_id
    ramassage.delete()
    messages.success(request, 'Ramassage d\'œufs supprimé avec succès.')
    return redirect('ramassage-list', lot_id=lot_id)

# HistoriqueTraitement Views


@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def historique_traitement_list_view(request, lot_id=None):
    queryset = HistoriqueTraitement.objects.filter(lot_id=lot_id) if lot_id else HistoriqueTraitement.objects.all()
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    if lot_id:
        queryset = queryset.filter(lot_id=lot_id)

    if date_min and date_max:
        queryset = queryset.filter(date_traitement__range=[date_min, date_max])

    create_form = HistoriqueTraitementForm(request.POST or None, lot_id=lot_id)
    if request.method == 'POST':
        if create_form.is_valid():
            historique = create_form.save(commit=False)
            historique.lot_id = lot_id
            historique.save()
            messages.success(request, 'Historique créée avec succès.')
            return redirect('historique-traitement-list', lot_id=lot_id)
        else:
            messages.error(request, 'Erreur lors de la création de l\'alimentation. Veuillez vérifier les données saisies.')


    context = {
        'historiques': queryset,
        'create_form': create_form,
        'lot_id': lot_id
    }
    return render(request, 'historique_traitement/historique_traitement_list.html', context)


# Vue pour mettre à jour un traitement historique

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def historique_traitement_update_view(request, pk):
    traitement = get_object_or_404(HistoriqueTraitement, pk=pk)
    form = HistoriqueTraitementForm(request.POST or None, instance=traitement)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Traitement historique mis à jour avec succès.')
            return redirect('historique-traitement-list')  # Remplacez 'historique-traitement-list' par le nom correct de l'URL de la liste
        else:
            messages.error(request, 'Erreur lors de la mise à jour du traitement historique. Veuillez vérifier les données saisies.')

    context = {
        'form': form,
    }
    return render(request, 'historique_traitement/historique_traitement_form.html', context)


# Vue pour supprimer un traitement historique
@login_required(login_url="/accounts/login/")
@require_POST
def historique_traitement_delete_view(request, pk):
    traitement = get_object_or_404(HistoriqueTraitement, pk=pk)
    lot_id = traitement.lot_id
    traitement.delete()
    messages.success(request, 'Traitement historique supprimé avec succès.')
    return redirect('historique-traitement-list',lot_id=lot_id)


# Provision Views
@login_required(login_url="/accounts/login/")
def provision_list_view(request):
    # Traitement des filtres
    aliment_id = request.GET.get('aliment_id', None)
    date_min = request.GET.get('date_min', None)
    date_max = request.GET.get('date_max', None)
    
    provisions = Provision.objects.all()
    if aliment_id:
        provisions = provisions.filter(aliment__nom=aliment_id)
    
    if date_min and date_max:
        provisions = provisions.filter(date_provision__range=[date_min, date_max])
    
    # Traitement des formulaires POST
    if request.method == 'POST':
        if 'create_provision' in request.POST:
            create_form = ProvisionForm(request.POST, request.FILES)
            if create_form.is_valid():
                create_form.save()
                messages.success(request, 'Provision créée avec succès.')
                return redirect(reverse('provision-list'))
            else:
                messages.error(request, 'Erreur lors de la création de la provision. Veuillez vérifier les données saisies.')
        elif 'delete_provision' in request.POST:
            provision_id = request.POST.get('provision_id')
            provision_instance = get_object_or_404(Provision, pk=provision_id)
            provision_instance.delete()
            messages.success(request, 'Provision supprimée avec succès.')
            return redirect(reverse('provision-list'))

    # Création du formulaire de création
    create_form = ProvisionForm()

    context = {
        'provisions': provisions,
        'create_form': create_form
    }
    
    return render(request, 'provision/provision_list.html', context)



class ProvisionCreateView(CreateView):
    model = Provision
    form_class = ProvisionForm
    template_name = 'provision/provision_form.html'
    success_url = reverse_lazy('provision-list')

@login_required(login_url="/accounts/login/")
def provision_update_view(request, pk):
    provision = get_object_or_404(Provision, pk=pk)
    if request.method == 'POST':
        form = ProvisionUpdateForm(request.POST, instance=provision)
        if form.is_valid():
            form.save()
            return redirect(reverse('provision-list'))
    else:
        form = ProvisionUpdateForm(instance=provision)
    
    return render(request, 'provision/provision_form.html', {'form': form})


class ProvisionDeleteView(DeleteView):
    model = Provision
    template_name = 'provision/provision_confirm_delete.html'
    success_url = reverse_lazy('provision-list')


 #-----------------------------------bases-----------------------------------------------

# Race Views
@login_required(login_url="/accounts/login/")
def race_list(request):
    races = Race.objects.all()
    create_form = RaceForm()  # Formulaire pour créer une nouvelle race

    # Récupérer les données du champ de recherche par nom
    query = request.GET.get('q', '')
    if query:
        races = races.filter(Q(nom__icontains=query))

    if request.method == 'POST':
        # Traitement pour la création d'une nouvelle race
        if 'create_race' in request.POST:
            create_form = RaceForm(request.POST, request.FILES)
            if create_form.is_valid():
                create_form.save()
                return redirect('race-list')  # Rediriger après la création

        # Traitement pour la suppression d'une race
        elif 'delete_race' in request.POST:
            race_id = request.POST.get('race_id')
            race_instance = get_object_or_404(Race, pk=race_id)
            race_instance.delete()
            return redirect('race-list')  # Rediriger après la suppression

    # Assurez-vous que edit_form est bien passé au contexte
    context = {
        'races': races,
        'create_form': create_form,
    }
    return render(request, 'races/race_list.html', context)


class RaceUpdateView(UpdateView):
    model = Race
    form_class = RaceForm
    template_name = 'races/race_form.html'
    success_url = reverse_lazy('race-list')

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def bande_list_view(request):
    queryset = Lot.objects.all()  # Adjust model if needed

    # Handle filtering
    name_filter = request.GET.get('nom', '')
    date_min = request.GET.get('date_min', '')
    date_max = request.GET.get('date_max', '')

    if name_filter:
        queryset = queryset.filter( nom__icontains=name_filter)
    
    if date_min:
        queryset = queryset.filter(date_arrivee__gte=date_min)
    
    if date_max:
        queryset = queryset.filter(date_arrivee__lte=date_max)
    
    # Handle form submission
    create_form = BandeForm(request.POST or None)
    if request.method == 'POST' and create_form.is_valid():
        create_form.save()
        messages.success(request, 'Bande créée avec succès.')
        return redirect('bande-list')
    elif request.method == 'POST':
        messages.error(request, 'Erreur lors de la création de la bande. Veuillez vérifier les données saisies.')

    context = {
        'bandes': queryset,
        'create_form': create_form,
        'segment': 'bandes'
    }
    return render(request, 'bandes/dashboard.html', context)



class BandeCreateView(CreateView):
    model = Lot
    form_class = BandeForm
    template_name = 'bandes/bande_form.html'
    success_url = reverse_lazy('bande-list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'bandes' 
        return context



class BandeUpdateView(UpdateView):
    model = Lot
    form_class = BandeUpdateForm
    template_name = 'bandes/bande_form.html'
    success_url = reverse_lazy('bande-list')



class BandeDeleteView(DeleteView):
    model = Lot
    template_name = 'bandes/bande_confirm_delete.html'
    success_url = reverse_lazy('bande-list')

# Aliment Views

class AlimentListView(ListView):
    model = Aliment
    template_name = 'aliments/aliment_list.html'
    context_object_name = 'aliments'

    def get_queryset(self):
        queryset = super().get_queryset()
        description = self.request.GET.get('description')
        date_min = self.request.GET.get('date_min')
        date_max = self.request.GET.get('date_max')

        if description:
            queryset = queryset.filter(nom__icontains=description)
        if date_min and date_max:
            queryset = queryset.filter(date__range=[date_min, date_max])

        return queryset

class AlimentCreateView(CreateView):
    model = Aliment
    form_class = AlimentForm
    template_name = 'aliments/aliment_form.html'
    success_url = reverse_lazy('aliment-list')


class AlimentUpdateView(UpdateView):
    model = Aliment
    form_class = AlimentForm
    template_name = 'aliments/aliment_form.html'
    success_url = reverse_lazy('aliment-list')


class AlimentDeleteView(DeleteView):
    model = Aliment
    template_name = 'aliments/aliment_confirm_delete.html'
    success_url = reverse_lazy('aliment-list')

# Traitement Views

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def traitement_list_view(request):
    # Initialiser les variables de filtrage
    date_min = request.GET.get('date_min', None)
    date_max = request.GET.get('date_max', None)
    description_query = request.GET.get('description', '')

    # Appliquer les filtres sur la queryset
    traitements = Traitement.objects.all()

    if date_min and date_max:
        traitements = traitements.filter(date_traitement__range=[date_min, date_max])

    if description_query:
        traitements = traitements.filter(nom__icontains=description_query)

    # Traitement du formulaire de création
    if request.method == "POST":
        create_form = TraitementForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            messages.success(request, 'Traitement créé avec succès.')
            return redirect('traitement-list')
        else:
            messages.error(request, 'Erreur lors de la création du traitement. Veuillez vérifier les données saisies.')
    else:
        create_form = TraitementForm()

    context = {
        'traitements': traitements,
        'create_form': create_form,
        'segment': 'traitements'
    }
    return render(request, 'traitements/traitement_list.html', context)

class TraitementCreateView(CreateView):
    model = Traitement
    form_class = TraitementForm
    template_name = 'traitements/traitement_form.html'
    success_url = reverse_lazy('traitement-list')



class TraitementUpdateView(UpdateView):
    model = Traitement
    form_class = TraitementForm
    template_name = 'traitements/traitement_form.html'
    success_url = reverse_lazy('traitement-list')


class TraitementDeleteView(DeleteView):
    model = Traitement
    template_name = 'traitements/traitement_confirm_delete.html'
    success_url = reverse_lazy('traitement-list')
