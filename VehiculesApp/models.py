from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator,MinValueValidator, MaxValueValidator

# Create your models here.

class Vehicule(models.Model):
    immaticulation = models.CharField(max_length = 10, unique =True, validators=[MinLengthValidator(1), MaxLengthValidator(10)])
    type_vehicule = models.CharField(max_length = 50, choices =[('camionette','camionette'),('fourgon','fourgon'),('camion_proteur','camion_proteur'),('semi_remorque','semi_remorque')])
    capacite_kg = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    entreprise = models.ForeignKey('EntrepriseApp.Entreprise', on_delete = models.CASCADE , related_name ='vehicules')

    
    def __str__(self):
        return "vehicules"

    def clean(self):
        if self.capacite_kg <= 0:
            raise ValidationError("La capacité du véhicule doit être supérieure à zéro.")