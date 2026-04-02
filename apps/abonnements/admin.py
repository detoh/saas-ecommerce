from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils import timezone
from .models import Abonnement

@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'plan', 'type_abo', 'prix', 'statut', 'date_debut', 'date_fin', 'est_actif')
    list_filter = ('statut', 'plan', 'type_abo', 'date_debut')
    search_fields = ('utilisateur__username', 'utilisateur__email', 'reference_paiement')
    readonly_fields = ('created_at', 'updated_at', 'est_actif', 'jours_restants', 'est_expirable_bientot')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('utilisateur', 'plan', 'type_abo', 'prix')
        }),
        ('Dates', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Statut', {
            'fields': ('statut', 'paiement_auto', 'reference_paiement')
        }),
        ('Informations système', {
            'fields': ('created_at', 'updated_at', 'est_actif', 'jours_restants', 'est_expirable_bientot'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activer_abonnements', 'expirer_abonnements']
    
    def activer_abonnements(self, request, queryset):
        for abonnement in queryset:
            abonnement.activer()
        self.message_user(request, f"{queryset.count()} abonnements activés")
    activer_abonnements.short_description = "Activer les abonnements sélectionnés"
    
    def expirer_abonnements(self, request, queryset):
        for abonnement in queryset:
            abonnement.expirer()
        self.message_user(request, f"{queryset.count()} abonnements expirés")
    expirer_abonnements.short_description = "Expirer les abonnements sélectionnés"