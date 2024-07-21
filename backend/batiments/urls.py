from django.urls import path
from .views import  BatimentCreateView, BatimentUpdateView
from . import views

urlpatterns = [
    path('', views.batiment_list_view, name='batiment-list'),
    path('ajouter/', BatimentCreateView.as_view(), name='batiment-create'),
    path('<int:pk>/modifier/', BatimentUpdateView.as_view(), name='batiment-update'),
    path('<int:pk>/supprimer/', views.batiment_delete_view, name='batiment-delete'),
    # other URLs...
]
