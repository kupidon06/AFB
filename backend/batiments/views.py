from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Batiment
from .forms import BatimentForm

@login_required(login_url="/accounts/login/")
@require_http_methods(["GET", "POST"])
def batiment_list_view(request):
    # Fetch all buildings initially
    batiments = Batiment.objects.all()

    # Handle search query
    search_query = request.GET.get('search', '')  # Retrieve search query from GET parameters
    if search_query:
        batiments = batiments.filter(nom__icontains=search_query)  # Filter buildings by name containing the search query

    # Handle form submission for creating new building
    create_form = BatimentForm(request.POST or None, request.FILES or None)  # Handle file uploads if any

    if request.method == 'POST':
        if create_form.is_valid():
            create_form.save()
            messages.success(request, 'Bâtiment créé avec succès.')
            return redirect('batiment-list')
        else:
            messages.error(request, 'Erreur lors de la création du bâtiment. Veuillez vérifier les données saisies.')

    context = {
        'batiments': batiments,
        'create_form': create_form,
        'segment': 'batiments'
    }
    return render(request, 'batiments/batiment_list.html', context)

class BatimentCreateView(CreateView):
    model = Batiment
    form_class = BatimentForm
    template_name = 'batiments/batiment_form.html'
    success_url = reverse_lazy('batiment_list')

class BatimentUpdateView(UpdateView):
    model = Batiment
    form_class = BatimentForm
    template_name = 'batiments/batiment_form.html'
    success_url = reverse_lazy('batiment_list')

require_POST
@login_required(login_url="/accounts/login/")
@require_POST
def batiment_delete_view(request, pk):
    batiment = get_object_or_404(Batiment, pk=pk)
    batiment.delete()
    messages.success(request, 'Bâtiment supprimé avec succès.')
    return redirect('batiment-list')
