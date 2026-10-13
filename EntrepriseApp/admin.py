from django.contrib import admin
from .models import utilisateur, Entreprise
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(utilisateur, UserAdmin)
admin.site.register(Entreprise)



class UtilisateurAdmin(UserAdmin):
    list_display = ('user_id', 'first_name', 'email', 'role', 'last_name')
    search_fields = ('user_id', 'first_name', 'email', 'role')
    list_filter = ('role',)
    ordering = ('telephone',)
    list_editable = ('first_name', 'email', 'role', 'last_name')
    ordering = ('user_id',)

class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'adresse', 'telephone')
    search_fields = ('nom', 'adresse')
    list_filter = ('nom',)
    ordering = ('id',)
