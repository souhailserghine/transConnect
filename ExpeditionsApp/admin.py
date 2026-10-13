from django.contrib import admin
from .models import Expedition
# Register your models here.
admin.site.register(Expedition)

from django.contrib.auth.admin import UserAdmin

class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'chargeur', 'transporteur', 'vehicule', 'poids_kg', 'date_expedition', 'status')
    search_fields = ('id', 'chargeur__username', 'transporteur__username', 'vehicule__immatriculation')
    list_filter = ('status',)
    ordering = ('date_expedition',)