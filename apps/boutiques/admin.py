from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Boutique

@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('nom_boutique', 'utilisateur', 'theme', 'devise', 'active', 'created_at')
    list_filter = ('theme', 'devise', 'created_at')
    search_fields = ('nom_boutique', 'utilisateur__username', 'utilisateur__email')
    readonly_fields = ('created_at', 'updated_at', 'active', 'url_boutique')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('utilisateur', 'nom_boutique', 'logo')
        }),
        ('Apparence', {
            'fields': ('theme', 'couleur_primaire', 'couleur_secondaire')
        }),
        ('Configuration', {
            'fields': ('devise', 'whatsapp_numero')
        }),
        ('Informations système', {
            'fields': ('active', 'url_boutique', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )