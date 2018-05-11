from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.db.models import Sum, Count
from django.db import models

import datetime

from django.utils import formats

from .models import Categorie
from .models import Etablissement
from .models import Transaction
from .models import Parametre
from django.db.models import When, F, Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required
def home_dynamic(request):

	report = '2'
	report = request.GET.get('choice', '2')

	jour=datetime.date.today()
	
	budget_parameters = Parametre.objects.all().annotate(mois=Sum('parametre_montant_hebdo') * 4).annotate(annee=Sum('parametre_montant_hebdo') * 52)

	if report == '1':
		categories = Categorie.objects.filter(etablissement__transaction__transaction_date=(jour)).annotate(somme_categ=Sum('etablissement__transaction__transaction_montant')).annotate(etat_budget = F('parametre__parametre_montant_hebdo') - Sum('etablissement__transaction__transaction_montant'))	
		periode_encours = jour

	elif report == '2':
		premier_jour = jour + datetime.timedelta(days=-((jour.weekday() + 2) % 7))
		dernier_jour= premier_jour + datetime.timedelta(days=6)
		categories = Categorie.objects.filter(etablissement__transaction__transaction_date__range=(premier_jour, dernier_jour)).annotate(somme_categ=Sum('etablissement__transaction__transaction_montant')).annotate(etat_budget = F('parametre__parametre_montant_hebdo') - Sum('etablissement__transaction__transaction_montant'))
		periode_encours = str(formats.date_format(premier_jour, 'l j')) + ' au ' + str(formats.date_format(dernier_jour, 'l j M Y'))

	elif report == '3':
		categories = Categorie.objects.filter(etablissement__transaction__transaction_date__month=jour.month).annotate(somme_categ=Sum('etablissement__transaction__transaction_montant')).annotate(etat_budget = F('parametre__parametre_montant_hebdo') * 4 - Sum('etablissement__transaction__transaction_montant'))
		periode_encours = jour

	elif report == '4':
		categories = Categorie.objects.filter(etablissement__transaction__transaction_date__year=jour.year).annotate(somme_categ=Sum('etablissement__transaction__transaction_montant')).annotate(etat_budget = F('parametre__parametre_montant_hebdo') * 52 - Sum('etablissement__transaction__transaction_montant'))
		periode_encours = jour

	context = {

		'categories' : categories,
		'periode_encours' : periode_encours,
		'report' : report,
		'budget_parameters' : budget_parameters,
	}

	return render(request, 'depenses/home_dynamic.html', context)

@login_required
def etablissements(request,categorie_id):

	report = '2'
	report = request.GET.get('choice', '2')
	
	jour=datetime.date.today()

	if report == '1':
		categorie_choisie = Categorie.objects.filter(id=categorie_id).filter(etablissement__transaction__transaction_date=(jour)).annotate(somme_categ=Sum('etablissement__transaction__transaction_montant'))
		etablissement_choisi = Etablissement.objects.filter(categorie=categorie_id).filter(transaction__transaction_date=(jour)).annotate(somme_etabliss=Sum('transaction__transaction_montant'))		
		periode_encours = jour

	elif report == '2':
		premier_jour = jour + datetime.timedelta(days=-((jour.weekday() + 2) % 7))
		dernier_jour= premier_jour + datetime.timedelta(days=6)
		categorie_choisie = Categorie.objects.filter(id=categorie_id).filter(etablissement__transaction__transaction_date__range=(premier_jour, dernier_jour)).annotate(somme_categ=Sum('etablissement__transaction__transaction_montant'))
		etablissement_choisi = Etablissement.objects.filter(categorie=categorie_id).filter(transaction__transaction_date__range=(premier_jour, dernier_jour)).annotate(somme_etabliss=Sum('transaction__transaction_montant'))		
		periode_encours = str(formats.date_format(premier_jour, 'l j')) + ' au ' + str(formats.date_format(dernier_jour, 'l j M Y'))	

	elif report == '3':
		categorie_choisie = Categorie.objects.filter(id=categorie_id).filter(etablissement__transaction__transaction_date__month=jour.month).annotate(somme_categ=Sum('etablissement__transaction__transaction_montant'))
		etablissement_choisi = Etablissement.objects.filter(categorie=categorie_id).filter(transaction__transaction_date__month=jour.month).annotate(somme_etabliss=Sum('transaction__transaction_montant'))
		periode_encours = jour

	elif report == '4':
		categorie_choisie = Categorie.objects.filter(id=categorie_id).filter(etablissement__transaction__transaction_date__year=jour.year).annotate(somme_categ=Sum('etablissement__transaction__transaction_montant'))
		etablissement_choisi = Etablissement.objects.filter(categorie=categorie_id).filter(transaction__transaction_date__year=jour.year).annotate(somme_etabliss=Sum('transaction__transaction_montant'))
		periode_encours = jour
	
	categorie_title = Categorie.objects.get(id=categorie_id)
	
	context = {
		'categorie_choisie' : categorie_choisie,
		'etablissement_choisi' : etablissement_choisi,
		'categorie_title' : categorie_title,
		'periode_encours' : periode_encours,
		'report' : report,
	}
	return render(request, 'depenses/etablissements_dynamic.html', context)

@login_required
def etablissement_details(request,etablissement_id):

	report = '2'
	report = request.GET.get('choice', '2')

	jour=datetime.date.today()

	if report == '1':
		transactions_etablissement = Transaction.objects.filter(etablissement=etablissement_id).filter(transaction_date=jour).order_by('transaction_date')
		periode_encours = jour

	elif report == '2':
		premier_jour = jour + datetime.timedelta(days=-((jour.weekday() + 2) % 7))
		dernier_jour= premier_jour + datetime.timedelta(days=6)
		transactions_etablissement = Transaction.objects.filter(etablissement=etablissement_id).filter(transaction_date__range=(premier_jour, dernier_jour)).order_by('transaction_date')
		periode_encours = str(formats.date_format(premier_jour, 'l j')) + ' au ' + str(formats.date_format(dernier_jour, 'l j M Y'))	

	elif report == '3':
		transactions_etablissement = Transaction.objects.filter(etablissement=etablissement_id).filter(transaction_date__month=(jour.month)).order_by('transaction_date')
		periode_encours = jour

	elif report == '4':
		transactions_etablissement = Transaction.objects.filter(etablissement=etablissement_id).filter(transaction_date__year=(jour.year)).order_by('transaction_date')
		periode_encours = jour

	etablissement_title = Etablissement.objects.get(pk=etablissement_id)

	context = {
		'transactions_etablissement' : transactions_etablissement,
		'periode_encours' : periode_encours,
		'etablissement_title' : etablissement_title,
		'report' : report,

	}
	return render(request, 'depenses/detail_etablissement_dynamic.html', context)

class TransactionCreate(LoginRequiredMixin,CreateView):
	model = Transaction
	fields = ['etablissement','transaction_date','transaction_montant']

class EtablissementCreate(LoginRequiredMixin,CreateView):
	model = Etablissement
	fields = ['categorie','etablissement_nom']

@login_required	
def nouvel_etablissement(request,etablissement_id):
	etablissement_cree = Etablissement.objects.get(id=etablissement_id)
	
	context = {
		'etablissement_cree' : etablissement_cree,
	}
	return render(request, 'depenses/etablissement_nouveau.html',context)

@login_required
def nouvelle_transaction(request,transaction_id):
	transaction_cree = Transaction.objects.get(id=transaction_id)
		
	context = {
		'transaction_cree' : transaction_cree,
	}
	return render(request, 'depenses/transaction_nouvelle.html',context)