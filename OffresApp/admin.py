from django.contrib import admin
from .models import Offre
# Register your models here.
admin.site.register(Offre)
from django.contrib.auth.admin import UserAdmin

class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'expedition', 'transporteur', 'prix', 'date_offre', 'status')
    search_fields = ('id', 'expedition__id', 'transporteur__username')
    list_filter = ('status',)
    ordering = ('date_offre',)