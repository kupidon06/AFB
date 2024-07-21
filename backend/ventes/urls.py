from django.urls import path
from . import views

urlpatterns = [
    
    
    # URL pour afficher la liste des ventes
    path('', views.vente_list_view, name='vente-list'),
    
    # URL pour mettre à jour une vente
    path('update/<int:pk>/', views.vente_update_view, name='vente-update'),
    
    # URL pour supprimer une vente
    path('delete/<int:pk>/', views.vente_delete_view, name='vente-delete'),


    path('charges/', views.charge_list_view, name='charge-list'),
    
    # URL pour mettre à jour une vente
    path('charges/update/<int:pk>/', views.charge_update_view, name='charge-update'),

    path('charge-categories/', views.charge_category_list_view, name='charge-category-list'),
    path('charge-categories/<int:pk>/update/', views.charge_category_update_view, name='charge-category-update'),


    path('poules/', views.poule_list_view, name='poule-list'),
    path('poules/<int:pk>/update/', views.poule_update_view, name='poule-update'),
    
    # URL patterns for Oeuf
    path('oeufs/', views.oeuf_list_view, name='oeuf-list'),
    path('oeufs/<int:pk>/update/', views.oeuf_update_view, name='oeuf-update'),

    
    
    # Autres URL pour remboursement et charge peuvent être ajoutées ici
]
