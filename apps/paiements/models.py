from django.db import models

# Create your models here.
from django.db import models
from apps.commandes.models import Commande
from django.utils import timezone

class Paiement(models.Model):
    METHODE_CHOICES = [
        ('orange_money', 'Orange Money'),
        ('wave', 'Wave'),
        ('mtn_money', 'MTN Money'),
        ('moov_money', 'Moov Money'),
        ('espece', 'Espèces à la livraison'),
    ]
    
    STATUT_CHOICES = [
        ('pending', 'En attente'),
        ('initiated', 'Initié'),
        ('success', 'Succès'),
        ('failed', 'Échoué'),
        ('cancelled', 'Annulé'),
        ('refunded', 'Remboursé'),
    ]
    
    commande = models.OneToOneField(
        Commande, 
        on_delete=models.CASCADE, 
        related_name='paiement'
    )
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode = models.CharField(max_length=50, choices=METHODE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    reference_interne = models.CharField(max_length=100, unique=True)
    telephone_paiement = models.CharField(max_length=20)
    operateur_response = models.JSONField(default=dict, blank=True)
    date_paiement = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    date_echec = models.DateTimeField(null=True, blank=True)
    frais_transaction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'paiements'
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-date_paiement']
    
    def __str__(self):
        return f"Paiement #{self.reference_interne} - {self.methode} - {self.statut}"
    
    def save(self, *args, **kwargs):
        # Générer une référence unique si elle n'existe pas
        if not self.reference_interne:
            prefix = self.methode.upper()[:3]
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.reference_interne = f"PAY-{prefix}-{timestamp}"
        super().save(*args, **kwargs)
    
    def initier_paiement(self):
        """Change le statut à 'initiated'"""
        self.statut = 'initiated'
        self.save()
    
    def confirmer_paiement(self, transaction_id=None):
        """Confirme le paiement avec succès"""
        self.statut = 'success'
        self.date_validation = timezone.now()
        if transaction_id:
            self.transaction_id = transaction_id
        self.save()
        
        # Mettre à jour la commande
        if self.commande:
            self.commande.statut = 'validee'
            self.commande.save()
    
    def echouer_paiement(self, reason=None):
        """Marque le paiement comme échoué"""
        self.statut = 'failed'
        self.date_echec = timezone.now()
        if reason:
            self.notes = reason
        self.save()
