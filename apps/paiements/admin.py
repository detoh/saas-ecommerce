from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('reference_interne', 'commande', 'methode', 'montant', 'statut', 'date_paiement')
    list_filter = ('methode', 'statut', 'date_paiement')
    search_fields = ('reference_interne', 'transaction_id', 'telephone_paiement')
    readonly_fields = ('reference_interne', 'date_paiement', 'date_validation', 'date_echec', 'operateur_response')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('reference_interne', 'commande', 'methode', 'montant')
        }),
        ('Statut', {
            'fields': ('statut', 'telephone_paiement')
        }),
        ('Transaction', {
            'fields': ('transaction_id', 'frais_transaction')
        }),
        ('Dates', {
            'fields': ('date_paiement', 'date_validation', 'date_echec')
        }),
        ('Réponse Opérateur', {
            'fields': ('operateur_response', 'notes'),
            'classes': ('collapse',)
        }),
    )
