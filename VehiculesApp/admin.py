from django.contrib import admin
from .models import vehicule
# Register your models here.
admin.site.register(vehicule)
from django.contrib.auth.admin import UserAdmin

class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('id', 'immatriculation', 'marque', 'modele', 'annee', 'charge_max')
    search_fields = ('id', 'immatriculation', 'marque', 'modele')
    list_filter = ('marque', 'modele', 'annee')
    ordering = ('id',)
