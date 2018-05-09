from django.contrib import admin
from .models import Categorie
from .models import Etablissement
from .models import Transaction
from .models import Parametre
# Register your models here.
admin.site.register(Categorie)
admin.site.register(Etablissement)
admin.site.register(Transaction)
admin.site.register(Parametre)