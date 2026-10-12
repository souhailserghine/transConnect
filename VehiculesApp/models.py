from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class vehicule(models.Model):
    TYPE_CHOICES = [
        ('camionnette', 'Camionnette / utilitaire léger'),
        ('camion_porteur', 'Camion porteur'),
        ('semi_remorque', 'Semi-remorque'),
        ('fourgon', 'Fourgon'),
    ]
    # Capacité indicative maximale (kg) par type, utilisée pour la compatibilité avec le poids d'une expédition
    CAPACITE_MAX_KG = {
        'camionnette': 1500,
        'fourgon': 3500,
        'camion_porteur': 19000,
        'semi_remorque': 26000,
    }
    immatriculation = models.CharField(max_length=10, unique=True)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacite_kg = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE, related_name='vehicules')

    def clean(self):
        # Seule une entreprise transporteur peut posséder des véhicules
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError({'entreprise': "Le véhicule doit appartenir à une entreprise de type transporteur."})

    def peut_transporter(self, poids_kg):
        # Règle 7 : le type du véhicule et sa capacité conditionnent le poids accepté
        return poids_kg <= self.CAPACITE_MAX_KG[self.type_vehicule] and poids_kg <= self.capacite_kg

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.immatriculation
