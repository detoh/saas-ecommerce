from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('en_attente', 'En attente'),
    ]
    
    telephone = models.CharField(max_length=20, blank=True)
    lien_site = models.CharField(max_length=100, unique=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'utilisateurs'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.username} ({self.lien_site})"