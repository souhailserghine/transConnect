from django.db import models

# Create your models here.
class Offer(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    Transporteur = models.ForeignKey('EntrepriseApp.Entreprise', on_delete = models.CASCADE , related_name ='transporteurs')
    Expedition=models.ForeignKey('ExpeditionsApp.Expedition', on_delete = models.CASCADE , related_name ='expeditions')
    Vehicule=models.ForeignKey('VehiculesApp.Vehicule', on_delete = models.CASCADE , related_name ='vehicules')

    
    def __str__(self):
        return "offre"