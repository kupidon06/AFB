from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('', include('dashboard.urls')),
    path('ventes/', include('ventes.urls')),
    path('produit/', include('produits.urls')),
    path('batiments/', include('batiments.urls')),
    path('clients/', include('clients.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
