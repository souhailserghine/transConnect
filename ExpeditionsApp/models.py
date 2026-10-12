from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Expedition(models.Model):
    reference =  models.CharField(max_length = 20 , unique = True)
    ville_depart =models.CharField(max_length=100)
    ville_arrive=models.CharField(max_length=100)
    date_souhaitee = models.DateField()
    poids_kg = models.DecimalField(max_digits=10,decimal_places=10)
    description = models.TextField()
    statut = models.CharField(choices=[
        ('publiee','publiee'),
        ('attribuee','attribuee'),
        ('en_cours','en_cours'),
        ('livree','livree'),
         ('annulee','annulee')
    ], default =  'publiee')
    entreprise = models.ForeignKey('EntrepriseApp.Entreprise', on_delete = models.CASCADE , related_name ='expeditions')

    