from django.conf.urls import url

from . import views

urlpatterns = [

    #/depenses/dynamic
    url(r'^dynamic/$', views.home_dynamic, name='home_dynamic'),

	#/depenses/etablissements/X
    url(r'^etablissements/(?P<categorie_id>[0-9]+)/$', views.etablissements, name='etablissements'),
    
    #/depenses/details/X
    url(r'^etablissements/details/(?P<etablissement_id>[0-9]+)/$',views.etablissement_details, name='etablissement_details'),

    #/depenses/transaction/add
    url(r'^transaction/add/$',views.TransactionCreate.as_view(),name='transaction_add'),

    #EtablissementCreate
    url(r'^etablissement/add/$',views.EtablissementCreate.as_view(),name='etablissement_add'),

    #/depenses/etablissements/nouveau/X
    url(r'^etablissements/nouveau/(?P<etablissement_id>[0-9]+)/$', views.nouvel_etablissement, name='nouvel_etablissement'),
 
    #/depenses/transaction/X
    url(r'^transaction/(?P<transaction_id>[0-9]+)/$', views.nouvelle_transaction, name='nouvelle_transaction'),

]