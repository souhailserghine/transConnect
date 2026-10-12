from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone


def valider_email_gmail(valeur):
    # Seuls les emails du domaine gmail.com sont acceptés
    if not valeur.lower().endswith('@gmail.com'):
        raise ValidationError("Seuls les emails du domaine gmail.com sont acceptés.")


# Matricule fiscal tunisien : 7 chiffres, clé, code TVA, catégorie, 3 chiffres
# Accepte 1234567AAM000, 1234567/A/A/M/000, 1234567-A-A-M-000 ou avec espaces
valider_matricule_fiscal = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
    message="Matricule fiscal invalide (ex. 1234567AAM000 ou 1234567/A/A/M/000).",
)


class utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur'),
        ('admin', 'Admin'),
    ]
    # Format AAuserNN : AA = année d'inscription, NN = compteur 00-99 remis à zéro chaque année
    user_id = models.CharField(max_length=8, editable=False, primary_key=True)
    email = models.EmailField(unique=True, validators=[valider_email_gmail])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='transporteur')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    telephone = models.CharField(max_length=8,blank=True,validators=[RegexValidator(r'^\d{8}$', "Le numéro de téléphone doit contenir 8 chiffres.")],)


    def generer_user_id(self):
        annee = (self.date_joined or timezone.now()).strftime('%y')
        prefixe = f"{annee}user"
        dernier = (utilisateur.objects.filter(user_id__startswith=prefixe)
                   .order_by('-user_id').values_list('user_id', flat=True).first())
        numero = int(dernier[-2:]) + 1 if dernier else 0
        if numero > 99:
            raise ValidationError(f"Plus de 100 inscriptions en 20{annee} : compteur user_id épuisé.")
        return f"{prefixe}{numero:02d}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.generer_user_id()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Entreprise(models.Model):
    TYPE_CHOICES = [
        ('chargeur', 'Chargeur'),
        ('transporteur', 'Transporteur'),
    ]
    raison_sociale = models.CharField(max_length=100)
    matricule_fiscal = models.CharField(max_length=17, unique=True, validators=[valider_matricule_fiscal])
    type_entreprise = models.CharField(max_length=20, choices=TYPE_CHOICES)
    adresse = models.TextField(validators=[MinLengthValidator(20)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    utilisateur = models.OneToOneField(utilisateur, on_delete=models.CASCADE, related_name='entreprise')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.raison_sociale
