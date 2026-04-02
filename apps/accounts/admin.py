from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'email', 'lien_site', 'statut', 'is_active')
    list_filter = ('statut', 'is_active')
    search_fields = ('username', 'email', 'lien_site', 'telephone')
    ordering = ('-date_creation',)
    
    # ✅ CORRECTION : Ne pas inclure date_creation dans les champs éditables
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'telephone', 'lien_site')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Statut', {'fields': ('statut',)}),
        # ✅ date_creation en readonly dans une section séparée
        ('Informations système', {'fields': ('date_creation',), 'classes': ('collapse',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'lien_site', 'statut'),
        }),
    )
    
    # ✅ Rendre date_creation en lecture seule
    readonly_fields = ('date_creation',)