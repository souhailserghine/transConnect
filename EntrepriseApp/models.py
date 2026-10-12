from django.db import models
from django.contrib.auth.models import AbstractUser


def email_validators(value):
    if not value.endswith('@gmail.com'):
        raise models.ValidationError("L'adresse e-mail doit se terminer par '@gmail.com'.") 


class Utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8,editable=False, primary_key=True)
    email= models.EmailField(unique=True,validators=[email_validators])
    role = models.CharField(max_length = 20 , choices =[('chargeur','chargeur'),('transorteur','transporteur'),('administrateur','administrateur')], default="chargeur")
    created_at = models .DateTimeField(auto_now_add = True)
    updated_at = models .DateTimeField(auto_now = True)
    telephone = models.CharField(max_length= 8)

class Entreprise(models.Model):
    raison_social = models.CharField(max_length = 100)
    matricule_fiscal = models.CharField(max_length = 8, unique =True)
    type_entreprise = models.CharField(max_length = 15 , choices=[('chargeur','chargeur'),('transporteur','transporteur')] )
    adresse = models.TextField()
    created_at = models .DateTimeField(auto_now_add = True)
    updated_at = models .DateTimeField(auto_now = True)
    gerant = models.OneToOneField(Utilisateur, on_delete= models.CASCADE, related_name='entreprise')

    def __str__(self):
        return "entreprise"