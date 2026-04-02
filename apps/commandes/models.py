from django.db import models

# Create your models here.
from django.db import models
from apps.boutiques.models import Boutique
from apps.produits.models import Produit
from django.utils import timezone

# ============================================
# 📌 CLIENT
# ============================================
class Client(models.Model):
    boutique = models.ForeignKey(
        Boutique, 
        on_delete=models.CASCADE, 
        related_name='clients'
    )
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'clients'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        unique_together = ['boutique', 'telephone']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nom} - {self.telephone}"

# ============================================
# 📌 COMMANDE
# ============================================
class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('en_preparation', 'En préparation'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]
    
    boutique = models.ForeignKey(
        Boutique, 
        on_delete=models.CASCADE, 
        related_name='commandes'
    )
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='commandes'
    )
    reference = models.CharField(max_length=50, unique=True, blank=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    frais_livraison = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=10, decimal_places=2)
    adresse_livraison = models.TextField()
    ville = models.CharField(max_length=100)
    telephone_livraison = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'commandes'
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-date_commande']
    
    def __str__(self):
        return f"Commande #{self.reference} - {self.client.nom}"
    
    def save(self, *args, **kwargs):
        # Générer une référence unique si elle n'existe pas
        if not self.reference:
            prefix = self.boutique.utilisateur.lien_site.upper()[:3]
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.reference = f"{prefix}-{timestamp}"
        
        # Calculer le total final
        self.total_final = self.total + self.frais_livraison
        super().save(*args, **kwargs)
    
    def calculer_total(self):
        """Calcule le total de la commande à partir des lignes"""
        total = sum(ligne.sous_total for ligne in self.lignes.all())
        self.total = total
        self.save()

# ============================================
# 📌 LIGNE DE COMMANDE
# ============================================
class LigneCommande(models.Model):
    commande = models.ForeignKey(
        Commande, 
        on_delete=models.CASCADE, 
        related_name='lignes'
    )
    produit = models.ForeignKey(
        Produit, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    nom_produit = models.CharField(max_length=200)  # Sauvegardé en cas de suppression du produit
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'lignes_commande'
        verbose_name = 'Ligne de commande'
        verbose_name_plural = 'Lignes de commande'
    
    def __str__(self):
        return f"{self.quantite}x {self.nom_produit}"
    
    def save(self, *args, **kwargs):
        self.sous_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)
