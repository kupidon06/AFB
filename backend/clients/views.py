from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client, Fournisseur
from .forms import ClientForm, FournisseurForm
from django.db.models import Q

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def client_list_view(request):
    queryset = Client.objects.all()
    query = request.GET.get('q')

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query)
        )

    if request.method == 'POST':
        if 'create' in request.POST:
            form = ClientForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Client créé avec succès.')
                return redirect('client-list')
            else:
                messages.error(request, 'Erreur lors de la création du client.')
    else:
        form = ClientForm()

    context = {
        'clients': queryset,
        'form': form,
    }
    return render(request, 'client/client_list.html', context)

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def client_update_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client mis à jour avec succès.')
            return redirect('client-list')
        else:
            messages.error(request, 'Erreur lors de la mise à jour du client.')
    else:
        form = ClientForm(instance=client)

    context = {
        'form': form,
    }
    return render(request, 'client/client_update.html', context)

@login_required(login_url="/accounts/login/")
@require_http_methods(["POST"])
def client_delete_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client supprimé avec succès.')
        return redirect('client-list')

    return redirect('client-list')





@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def fournisseur_list_view(request):
    queryset = Fournisseur.objects.all()
    query = request.GET.get('q')

    if query:
        queryset = queryset.filter(
            Q(nom__icontains=query) |
            Q(contact__icontains=query)
        )

    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fournisseur créé avec succès.')
            return redirect('fournisseur-list')
        else:
            messages.error(request, 'Erreur lors de la création du fournisseur.')
    else:
        form = FournisseurForm()

    context = {
        'fournisseurs': queryset,
        'form': form,
    }
    return render(request, 'fournisseur/fournisseur_list.html', context)


@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def fournisseur_update_view(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fournisseur mis à jour avec succès.')
            return redirect('fournisseur-list')
        else:
            messages.error(request, 'Erreur lors de la mise à jour du fournisseur.')
    else:
        form = FournisseurForm(instance=fournisseur)

    context = {
        'form': form,
        'fournisseur': fournisseur,
    }
    return render(request, 'fournisseur/fournisseur_update.html', context)


@login_required(login_url="/accounts/login/")
@require_http_methods(["POST"])
def fournisseur_delete_view(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    fournisseur.delete()
    messages.success(request, 'Fournisseur supprimé avec succès.')
    return redirect('fournisseur-list')
