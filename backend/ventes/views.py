from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import formset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import VenteForm, VenteItemForm, RemboursementForm, ChargeForm,ChargeCategoryForm,PouleForm,OeufForm
from .operations import Vente, VenteItem, Remboursement, Charge
from .models import Poule,Oeuf,ChargeCategory
from clients.models import Client

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def vente_list_view(request):
    VenteItemFormSet = formset_factory(VenteItemForm, extra=1)  # Formset for vente items

    if request.method == 'POST':
        if 'create_vente' in request.POST:
            vente_form = VenteForm(request.POST)
            formset = VenteItemFormSet(request.POST)

            if vente_form.is_valid() and formset.is_valid():
                vente = vente_form.save()
                for form in formset:
                    if form.cleaned_data:
                        vente_item = form.save(commit=False)
                        vente_item.vente = vente
                        vente_item.save()
                messages.success(request, 'Vente et items créés avec succès.')
                return redirect('vente-list')
            else:
                print("Vente form errors:", vente_form.errors)
                print("Formset errors:", formset.errors)
                messages.error(request, 'Erreur lors de la création de la vente et des items.')
        else:
            vente_form = VenteForm()
            formset = VenteItemFormSet(request.POST)

    else:
        vente_form = VenteForm()
        formset = VenteItemFormSet()

    # Apply filtering based on GET parameters
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    ventes = Vente.objects.all()

    if query:
        client_ids = Client.objects.filter(name__icontains=query).values_list('id', flat=True)
        ventes = ventes.filter(client_id__in=client_ids)

    if start_date:
        ventes = ventes.filter(date_vente__gte=start_date)
    
    if end_date:
        ventes = ventes.filter(date_vente__lte=end_date)

    clients = Client.objects.all()  # Fetch all clients for the search input

    context = {
        'ventes': ventes,
        'vente_form': vente_form,
        'formset': formset # Add clients to the context
    }
    return render(request, 'ventes/vente_list.html', context)


@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def vente_update_view(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    VenteItemFormSet = inlineformset_factory(Vente, VenteItem, form=VenteItemForm, extra=1, can_delete=True)

    if request.method == 'POST':
        vente_form = VenteForm(request.POST, instance=vente)
        formset = VenteItemFormSet(request.POST, instance=vente)
        
        if vente_form.is_valid() and formset.is_valid():
            vente = vente_form.save()
            formset.instance = vente
            formset.save()
            messages.success(request, 'Vente mise à jour avec succès.')
            return redirect('vente-list')
        else:
            messages.error(request, 'Erreur lors de la mise à jour de la vente.')
            print(vente_form.errors)
            print(formset.errors)
    else:
        vente_form = VenteForm(instance=vente)
        formset = VenteItemFormSet(instance=vente)

    context = {
        'vente_form': vente_form,
        'formset': formset,
    }
    return render(request, 'ventes/vente_update.html', context)




@login_required(login_url="/accounts/login/")
@require_http_methods(["POST"])
def vente_delete_view(request, pk=None):
    vente_id = request.POST.get('vente_id')
    if vente_id:
        vente = get_object_or_404(Vente, pk=vente_id)
        vente.delete()
        messages.success(request, 'Vente supprimée avec succès.')
    else:
        messages.error(request, 'Erreur lors de la suppression de la vente.')
    return redirect('vente-list')


@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def remboursement_create_view(request):
    if request.method == 'POST':
        form = RemboursementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Remboursement créé avec succès.')
            return redirect('remboursement-list')  # Modifier selon votre URL de redirection
        else:
            messages.error(request, 'Erreur lors de la création du remboursement.')
    else:
        form = RemboursementForm()

    context = {
        'form': form,
    }
    return render(request, 'remboursement/remboursement_create.html', context)

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def remboursement_update_view(request, pk):
    remboursement = get_object_or_404(Remboursement, pk=pk)

    if request.method == 'POST':
        form = RemboursementForm(request.POST, instance=remboursement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Remboursement mis à jour avec succès.')
            return redirect('remboursement-list')  # Modifier selon votre URL de redirection
        else:
            messages.error(request, 'Erreur lors de la mise à jour du remboursement.')
    else:
        form = RemboursementForm(instance=remboursement)

    context = {
        'form': form,
    }
    return render(request, 'remboursement/remboursement_update.html', context)

@login_required(login_url="/accounts/login/")
@require_http_methods(["POST"])
def remboursement_delete_view(request, pk):
    remboursement = get_object_or_404(Remboursement, pk=pk)
    remboursement.delete()
    messages.success(request, 'Remboursement supprimé avec succès.')
    return redirect('remboursement-list')  # Modifier selon votre URL de redirection

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def charge_list_view(request):
    if request.method == 'POST':
        if 'create_charge' in request.POST:
            form = ChargeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Charge créée avec succès.')
                return redirect('charge-list')
            else:
                messages.error(request, 'Erreur lors de la création de la charge.')
        elif 'delete_charge' in request.POST:
            charge_id = request.POST.get('charge_id')
            if charge_id:
                charge = get_object_or_404(Charge, id=charge_id)
                charge.delete()
                messages.success(request, 'Charge supprimée avec succès.')
                return redirect('charge-list')
    else:
        form = ChargeForm()

    # Apply filtering based on GET parameters
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    charges = Charge.objects.all()

    if query:
        charges = charges.filter(category__nom__icontains=query)  # Assuming 'name' is the field to search

    if start_date:
        charges = charges.filter(date_charge__gte=start_date)
    
    if end_date:
        charges = charges.filter(date_charge__lte=end_date)

    context = {
        'charges': charges,
        'form': form,
    }
    return render(request, 'charge/charge_list.html', context)


@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def charge_update_view(request, pk):
    charge = get_object_or_404(Charge, pk=pk)

    if request.method == 'POST':
        form = ChargeForm(request.POST, instance=charge)
        if form.is_valid():
            form.save()
            messages.success(request, 'Charge mise à jour avec succès.')
            return redirect('charge-list')
        else:
            messages.error(request, 'Erreur lors de la mise à jour de la charge.')
    else:
        form = ChargeForm(instance=charge)

    context = {
        'form': form,
    }
    return render(request, 'charge/charge_update.html', context)

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def charge_category_list_view(request):
    categories = ChargeCategory.objects.all()

    if request.method == 'POST':
        if 'create_charge_category' in request.POST:
            form = ChargeCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Catégorie de charge créée avec succès.')
                return redirect('charge-category-list')
            else:
                messages.error(request, 'Erreur lors de la création de la catégorie de charge.')
        elif 'delete_charge_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(ChargeCategory, id=category_id)
            category.delete()
            messages.success(request, 'Catégorie de charge supprimée avec succès.')
            return redirect('charge-category-list')
    else:
        form = ChargeCategoryForm()

    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'charge/charge_category_list.html', context)



@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def charge_category_update_view(request, pk):
    category = get_object_or_404(ChargeCategory, pk=pk)

    if request.method == 'POST':
        form = ChargeCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie de charge mise à jour avec succès.')
            return redirect('charge-category-list')
        else:
            messages.error(request, 'Erreur lors de la mise à jour de la catégorie de charge.')
    else:
        form = ChargeCategoryForm(instance=category)

    context = {
        'form': form,
    }
    return render(request, 'charge/charge_category_update.html', context)


@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def poule_list_view(request):
    poules = Poule.objects.all()

    if request.method == 'POST':
        if 'create_poule' in request.POST:
            form = PouleForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Poules créée avec succès.')
                return redirect('poule-list')
            else:
                messages.error(request, 'Erreur lors de la création de la poule.')
        elif 'delete_poule' in request.POST:
            poule_id = request.POST.get('poule_id')
            poule = get_object_or_404(Poule, id=poule_id)
            poule.delete()
            messages.success(request, 'Poules supprimée avec succès.')
            return redirect('poule-list')
    else:
        form = PouleForm()

    context = {
        'poules': poules,
        'form': form,
    }
    return render(request, 'poule/poule_list.html', context)

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def poule_update_view(request, pk):
    poule = get_object_or_404(Poule, pk=pk)

    if request.method == 'POST':
        form = PouleForm(request.POST, request.FILES, instance=poule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poules mise à jour avec succès.')
            return redirect('poule-list')
        else:
            messages.error(request, 'Erreur lors de la mise à jour de la poule.')
    else:
        form = PouleForm(instance=poule)

    context = {
        'form': form,
    }
    return render(request, 'poule/poule_update.html', context)

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def oeuf_list_view(request):
    oeufs = Oeuf.objects.all()

    if request.method == 'POST':
        if 'create_oeuf' in request.POST:
            form = OeufForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Œuf créé avec succès.')
                return redirect('oeuf-list')
            else:
                messages.error(request, 'Erreur lors de la création de l’œuf.')
        elif 'delete_oeuf' in request.POST:
            oeuf_id = request.POST.get('oeuf_id')
            oeuf = get_object_or_404(Oeuf, id=oeuf_id)
            oeuf.delete()
            messages.success(request, 'Œuf supprimé avec succès.')
            return redirect('oeuf-list')
    else:
        form = OeufForm()

    context = {
        'oeufs': oeufs,
        'form': form,
    }
    return render(request, 'oeuf/oeuf_list.html', context)

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def oeuf_update_view(request, pk):
    oeuf = get_object_or_404(Oeuf, pk=pk)

    if request.method == 'POST':
        form = OeufForm(request.POST, request.FILES, instance=oeuf)
        if form.is_valid():
            form.save()
            messages.success(request, 'Œuf mis à jour avec succès.')
            return redirect('oeuf-list')
        else:
            messages.error(request, 'Erreur lors de la mise à jour de l’œuf.')
    else:
        form = OeufForm(instance=oeuf)

    context = {
        'form': form,
    }
    return render(request, 'oeuf/oeuf_update.html', context)