from django.db import models
from apps.boutiques.models import Boutique

class Categorie(models.Model):
    boutique = models.ForeignKey(
        Boutique,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='enfants'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['nom']
        unique_together = ['boutique', 'slug']
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    @property
    def nombre_produits(self):
        return self.produits.filter(is_visible=True).count()

class Produit(models.Model):
    CATEGORIE_CHOICES = [
        ('vetements', 'Vêtements'),
        ('chaussures', 'Chaussures'),
        ('accessoires', 'Accessoires'),
        ('electronique', 'Électronique'),
        ('maison', 'Maison'),
        ('beaute', 'Beauté'),
        ('autre', 'Autre'),
    ]
    
    boutique = models.ForeignKey(
        Boutique, 
        on_delete=models.CASCADE, 
        related_name='produits'
    )
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    images_supplementaires = models.JSONField(default=list, blank=True)
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produits'
    )
    categorie_nom = models.CharField(max_length=100, blank=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'produits'
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nom} - {self.boutique.nom_boutique}"
    
    @property
    def prix_actuel(self):
        return self.prix_promo if self.prix_promo and self.prix_promo < self.prix else self.prix
    
    @property
    def en_stock(self):
        return self.stock > 0
    
    @property
    def pourcentage_reduction(self):
        if self.prix_promo and self.prix_promo < self.prix:
            reduction = ((self.prix - self.prix_promo) / self.prix) * 100
            return round(reduction, 2)
        return 0
    
    @property
    def toutes_les_images(self):
        """Retourne toutes les images (principale + supplémentaires)"""
        images = []
        if self.image:
            images.append(self.image.url)
        if self.images_supplementaires:
            images.extend(self.images_supplementaires)
        return images