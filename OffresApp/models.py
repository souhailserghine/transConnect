from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from ExpeditionsApp.models import Expedition, valider_strictement_positif


class Offre(models.Model):
    STATUT_CHOICES = [
        ('proposee', 'Proposée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('retiree', 'Retirée'),
    ]
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[valider_strictement_positif])
    delai_jours = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='proposee')
    date_proposition = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expedition = models.ForeignKey('ExpeditionsApp.Expedition', on_delete=models.CASCADE, related_name='offres')
    transporteur = models.ForeignKey('EntrepriseApp.Entreprise', on_delete=models.CASCADE, related_name='offres')
    vehicule = models.ForeignKey('VehiculesApp.vehicule', on_delete=models.CASCADE, related_name='offres')

    def clean(self):
        erreurs = {}
        nouvelle = self._state.adding

        if self.transporteur_id:
            # Règle 1 : seule une entreprise transporteur peut proposer une offre
            if self.transporteur.type_entreprise != 'transporteur':
                erreurs['transporteur'] = "Seule une entreprise de type transporteur peut proposer une offre."
            # Règle 2 : le véhicule doit appartenir au transporteur de l'offre
            elif self.vehicule_id and self.vehicule.entreprise_id != self.transporteur_id:
                erreurs['vehicule'] = "Le véhicule doit appartenir à l'entreprise qui propose l'offre."

        if nouvelle and self.expedition_id and self.expedition.statut != 'publiee':
            # Règle 3 : seules les expéditions publiées reçoivent de nouvelles offres
            erreurs['expedition'] = "Cette expédition n'accepte plus de nouvelles offres (statut différent de publiée)."

        if self.statut == 'proposee' and self.expedition_id and self.transporteur_id:
            # Règle 4 : une seule offre proposée par entreprise et par expédition
            doublon = Offre.objects.filter(
                expedition_id=self.expedition_id, transporteur_id=self.transporteur_id, statut='proposee'
            ).exclude(pk=self.pk)
            if doublon.exists():
                erreurs['__all__'] = "Cette entreprise a déjà une offre proposée sur cette expédition."

        if self.vehicule_id:
            # Règle 6 : un véhicule indisponible ne peut pas être proposé
            if nouvelle and not self.vehicule.disponible:
                erreurs['vehicule'] = "Ce véhicule n'est pas disponible."
            # Règle 7 : le type et la capacité du véhicule doivent couvrir le poids de l'expédition
            elif self.expedition_id and not self.vehicule.peut_transporter(self.expedition.poids_kg):
                erreurs['vehicule'] = (
                    f"Un véhicule de type {self.vehicule.get_type_vehicule_display()} "
                    f"({self.vehicule.capacite_kg} kg) ne peut pas transporter {self.expedition.poids_kg} kg."
                )

        if erreurs:
            raise ValidationError(erreurs)

    def save(self, *args, **kwargs):
        self.full_clean()
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.statut == 'acceptee':
                # Règle 5 : cascade à l'acceptation
                # update() écrit directement en base, sans repasser par save()/clean()
                Expedition.objects.filter(pk=self.expedition_id).update(statut='attribuee')
                self.expedition.statut = 'attribuee'
                Offre.objects.filter(expedition_id=self.expedition_id, statut='proposee') \
                    .exclude(pk=self.pk).update(statut='refusee')

    def __str__(self):
        return f"Offre {self.id} - Expedition {self.expedition.reference} - Transporteur {self.transporteur.raison_sociale}"
