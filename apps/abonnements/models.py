from django.db import models
from apps.accounts.models import Utilisateur
from django.utils import timezone
from datetime import timedelta

class Abonnement(models.Model):
    TYPE_CHOICES = [
        ('mensuel', 'Mensuel'),
        ('trimestriel', 'Trimestriel'),
        ('annuel', 'Annuel'),
    ]
    
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('expire', 'Expiré'),
        ('impaye', 'Impayé'),
        ('annule', 'Annulé'),
        ('essai', 'Période d\'essai'),
    ]
    
    PLAN_CHOICES = [
        ('basic', 'Basic - 10 000 FCFA/mois'),
        ('pro', 'Pro - 25 000 FCFA/mois'),
        ('premium', 'Premium - 50 000 FCFA/mois'),
    ]
    
    id_abonnement = models.BigAutoField(primary_key=True)
    utilisateur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='abonnements'
    )
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES, default='basic')
    type_abo = models.CharField(max_length=50, choices=TYPE_CHOICES, default='mensuel')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='impaye')
    paiement_auto = models.BooleanField(default=False)
    reference_paiement = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'abonnements'
        verbose_name = 'Abonnement'
        verbose_name_plural = 'Abonnements'
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"Abonnement {self.utilisateur.username} - {self.plan} ({self.date_debut} au {self.date_fin})"
    
    def save(self, *args, **kwargs):
        # Calculer la date de fin selon le type
        if not self.date_fin and self.date_debut:
            if self.type_abo == 'mensuel':
                self.date_fin = self.date_debut + timedelta(days=30)
            elif self.type_abo == 'trimestriel':
                self.date_fin = self.date_debut + timedelta(days=90)
            elif self.type_abo == 'annuel':
                self.date_fin = self.date_debut + timedelta(days=365)
        super().save(*args, **kwargs)
    
    @property
    def est_actif(self):
        """Vérifie si l'abonnement est actif"""
        if not self.date_fin:
            return False
        return self.statut == 'actif' and self.date_fin >= timezone.now().date()
    
    @property
    def jours_restants(self):
        """Calcule les jours restants avant expiration"""
        if not self.date_fin:
            return 0
        if self.date_fin >= timezone.now().date():
            return (self.date_fin - timezone.now().date()).days
        return 0
    
    @property
    def est_expirable_bientot(self):
        """Vérifie si l'abonnement expire dans moins de 7 jours"""
        if not self.date_fin:
            return False
        return self.jours_restants <= 7 and self.jours_restants >= 0
    
    def activer(self):
        """Active l'abonnement"""
        self.statut = 'actif'
        self.save()
    
    def expirer(self):
        """Expire l'abonnement"""
        self.statut = 'expire'
        self.save()
        
        # Suspendre l'utilisateur
        self.utilisateur.statut = 'suspendu'
        self.utilisateur.save()
    
    def renouveler(self, type_abo=None):
        """Renouvelle l'abonnement"""
        if type_abo:
            self.type_abo = type_abo
        
        self.date_debut = timezone.now().date()
        
        if self.type_abo == 'mensuel':
            self.date_fin = self.date_debut + timedelta(days=30)
        elif self.type_abo == 'trimestriel':
            self.date_fin = self.date_debut + timedelta(days=90)
        elif self.type_abo == 'annuel':
            self.date_fin = self.date_debut + timedelta(days=365)
        
        self.statut = 'actif'
        self.save()