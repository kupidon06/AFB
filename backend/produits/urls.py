# urls.py
from django.urls import path
from .views import (
    race_list,RaceUpdateView,
    BandeUpdateView, BandeDeleteView,
    AlimentListView, AlimentCreateView, AlimentUpdateView, AlimentDeleteView,
     TraitementUpdateView, TraitementDeleteView,
    ProvisionCreateView,  ProvisionDeleteView,
)
from . import views


urlpatterns = [
    # Race URLs
    path('races/', race_list, name='race-list'),
    path('races/<int:pk>/update/', RaceUpdateView.as_view(), name='race-update'),

    # Bande URLs
    path('lots/', views.bande_list_view, name='bande-list'),
    path('lots/<int:pk>/update/', BandeUpdateView.as_view(), name='bande-update'),
    path('lots/<int:pk>/delete/', BandeDeleteView.as_view(), name='bande-delete'),

    # Aliment URLs
    path('aliments/', AlimentListView.as_view(), name='aliment-list'),
    path('aliments/create/', AlimentCreateView.as_view(), name='aliment-create'),
    path('aliments/<int:pk>/update/', AlimentUpdateView.as_view(), name='aliment-update'),
    path('aliments/<int:pk>/delete/', AlimentDeleteView.as_view(), name='aliment-delete'),

    # Traitement URLs
    path('traitements/', views.traitement_list_view, name='traitement-list'),
    path('traitements/<int:pk>/update/', TraitementUpdateView.as_view(), name='traitement-update'),
    path('traitements/<int:pk>/delete/', TraitementDeleteView.as_view(), name='traitement-delete'),
    #-------------------------------------------operations------------------------------------------------------
    # JournalisationQuotidienne URLs
    path('journalisation/', views.journalisation_quotidienne_list_view, name='journalisation-list'),
    path('journalisation/<int:lot_id>/', views.journalisation_quotidienne_list_view, name='journalisation-list'),
    path('journalisation/<int:pk>/update/', views.journalisation_quotidienne_update_view, name='journalisation-update'),
    path('journalisation/<int:pk>/delete/', views.journalisation_quotidienne_delete_view, name='journalisation-delete'),


    # Alimentation URLs
    path('alimentation/', views.alimentation_list_view, name='alimentation-list'),
     path('alimentation/<int:lot_id>/', views.alimentation_list_view, name='alimentation-list'),
    path('alimentation/<int:pk>/update/', views.alimentation_update_view, name='alimentation-update'),
    path('alimentation/<int:pk>/delete/', views.alimentation_delete_view, name='alimentation-delete'),


    # RamassageOeufs URLs
    path('ramassage/', views.ramassage_oeufs_list_view, name='ramassage-list'),
    path('ramassage/<int:lot_id>/', views.ramassage_oeufs_list_view, name='ramassage-list'),
    path('ramassage/<int:pk>/update/', views.ramassage_oeufs_update_view, name='ramassage-update'),
    path('ramassage/<int:pk>/delete/', views.ramassage_oeufs_delete_view, name='ramassage-delete'),


    # HistoriqueTraitement URLs
    path('historique-traitement/', views.historique_traitement_list_view, name='historique-traitement-list'),
    path('historique-traitement/<int:lot_id>/', views.historique_traitement_list_view, name='historique-traitement-list'),
    path('historique-traitement/<int:pk>/update/', views.historique_traitement_update_view, name='historique-traitement-update'),
    path('historique-traitement/<int:pk>/delete/', views.historique_traitement_delete_view, name='historique-traitement-delete'),

    # Provision URLs
    path('provisions/', views.provision_list_view, name='provision-list'),
    path('provisions/create/', ProvisionCreateView.as_view(), name='provision-create'),
    path('provisions/<int:pk>/update/', views.provision_update_view, name='provision-update'),
    path('provisions/<int:pk>/delete/', ProvisionDeleteView.as_view(), name='provision-delete'),
]
