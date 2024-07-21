from django.contrib import admin
from .models import Batiment

@admin.register(Batiment)
class BatimentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'capacite',)
    list_filter = ('capacite',)
    search_fields = ('nom',)
