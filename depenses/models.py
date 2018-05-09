from datetime import date
from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Categorie(models.Model):
	categorie_nom = models.CharField(max_length=100)
	def __str__(self):
	   	return self.categorie_nom

class Etablissement(models.Model):
	categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
	etablissement_nom = models.CharField(max_length=100, unique=True, db_index=True)

	def get_absolute_url(self):
		return reverse('nouvel_etablissement',kwargs={'etablissement_id':self.id})
	
	def __str__(self):
	   	return self.etablissement_nom

	def clean(self):
		self.etablissement_nom = self.etablissement_nom.capitalize()

class Transaction(models.Model):
	etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE)
	transaction_date = models.DateField(default=date.today())
	transaction_montant = models.DecimalField(max_digits=6, decimal_places=2)

	def get_absolute_url(self):
		return reverse('nouvelle_transaction',kwargs={'transaction_id':self.id})

	def __str__(self):
		return self.etablissement.etablissement_nom

class Parametre(models.Model):
	parametre_type = models.ForeignKey(Categorie, on_delete=models.CASCADE)
	parametre_nom = models.CharField(max_length=100, unique=True, db_index=True)
	parametre_montant_hebdo = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return self.parametre_nom