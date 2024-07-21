from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list_view, name='client-list'),
    path('update/<int:pk>/', views.client_update_view, name='client-update'),
    path('delete/<int:pk>/', views.client_delete_view, name='client-delete'),

    path('fournisseurs/', views.fournisseur_list_view, name='fournisseur-list'),
    path('fournisseurs/<int:pk>/update/', views.fournisseur_update_view, name='fournisseur-update'),
    path('fournisseurs/<int:pk>/delete/', views.fournisseur_delete_view, name='fournisseur-delete'),

]
