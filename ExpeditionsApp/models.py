from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


def valider_strictement_positif(valeur):
    if valeur is not None and valeur <= 0:
        raise ValidationError("La valeur doit être strictement supérieure à 0.")


class Expedition(models.Model):
    STATUT_CHOICES = [
        ('publiee', 'Publiée'),
        ('attribuee', 'Attribuée'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]
    # Format EXP-AA-NNNNN : AA = année de création, NNNNN = compteur 00001-99999 remis à zéro chaque année
    reference = models.CharField(max_length=12, unique=True, editable=False)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[valider_strictement_positif])
    date_souhaitee = models.DateField()
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='publiee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE, related_name='expeditions')

    def generer_reference(self):
        annee = timezone.now().strftime('%y')
        prefixe = f"EXP-{annee}-"
        derniere = (Expedition.objects.filter(reference__startswith=prefixe)
                    .order_by('-reference').values_list('reference', flat=True).first())
        numero = int(derniere[-5:]) + 1 if derniere else 1
        if numero > 99999:
            raise ValidationError(f"Compteur de références épuisé pour 20{annee}.")
        return f"{prefixe}{numero:05d}"

    def clean(self):
        # Seule une entreprise chargeur peut publier une expédition
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({'entreprise': "L'expédition doit être publiée par une entreprise de type chargeur."})

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generer_reference()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference
