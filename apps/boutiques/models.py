from django.db import models

# Create your models here.
from django.db import models
from apps.accounts.models import Utilisateur
from django.utils import timezone

class Boutique(models.Model):
    THEME_CHOICES = [
        ('default', 'Défaut'),
        ('moderne', 'Moderne'),
        ('minimaliste', 'Minimaliste'),
        ('colore', 'Coloré'),
    ]
    
    utilisateur = models.OneToOneField(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='boutique'
    )
    nom_boutique = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default='default')
    couleur_primaire = models.CharField(max_length=7, default='#000000')
    couleur_secondaire = models.CharField(max_length=7, default='#FFFFFF')
    devise = models.CharField(max_length=3, default='XOF')
    whatsapp_numero = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'boutiques'
        verbose_name = 'Boutique'
        verbose_name_plural = 'Boutiques'
    
    def __str__(self):
        return self.nom_boutique
    
    @property
    def active(self):
        """Vérifie si la boutique est active (abonnement valide)"""
        try:
            from apps.abonnements.models import Abonnement
            abo_actif = self.utilisateur.abonnements.filter(
                statut='actif',
                date_fin__gte=timezone.now().date()
            ).first()
            return abo_actif is not None and self.utilisateur.statut == 'actif'
        except:
            return self.utilisateur.statut == 'actif'
    
    @property
    def url_boutique(self):
        return f"/{self.utilisateur.lien_site}"