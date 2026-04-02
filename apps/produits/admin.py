from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Produit

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'boutique', 'prix', 'prix_promo', 'stock', 'categorie', 'is_visible', 'created_at')
    list_filter = ('categorie', 'is_visible', 'created_at')
    search_fields = ('nom', 'description', 'boutique__nom_boutique')
    readonly_fields = ('created_at', 'updated_at', 'prix_actuel', 'en_stock')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('boutique', 'nom', 'description', 'categorie')
        }),
        ('Prix et Stock', {
            'fields': ('prix', 'prix_promo', 'stock')
        }),
        ('Images', {
            'fields': ('image', 'images_supplementaires')
        }),
        ('Options', {
            'fields': ('is_visible',)
        }),
        ('Informations système', {
            'fields': ('created_at', 'updated_at', 'prix_actuel', 'en_stock'),
            'classes': ('collapse',)
        }),
    )
