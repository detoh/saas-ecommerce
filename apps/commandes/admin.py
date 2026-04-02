from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Client, Commande, LigneCommande

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telephone', 'email', 'boutique', 'created_at')
    list_filter = ('boutique', 'created_at')
    search_fields = ('nom', 'telephone', 'email')

class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0
    readonly_fields = ('sous_total',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('reference', 'client', 'boutique', 'statut', 'total_final', 'date_commande')
    list_filter = ('statut', 'boutique', 'date_commande')
    search_fields = ('reference', 'client__nom', 'client__telephone')
    readonly_fields = ('reference', 'date_commande', 'total', 'total_final')
    inlines = [LigneCommandeInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('reference', 'boutique', 'client', 'date_commande', 'statut')
        }),
        ('Livraison', {
            'fields': ('adresse_livraison', 'ville', 'telephone_livraison')
        }),
        ('Paiement', {
            'fields': ('total', 'frais_livraison', 'total_final')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )