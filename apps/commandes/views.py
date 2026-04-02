from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Client, Commande, LigneCommande
from .serializers import (
    ClientSerializer, CommandeSerializer, CommandeCreateSerializer,
    CommandeListSerializer
)

class CommandePermission(permissions.BasePermission):
    """Permission personnalisée pour les commandes"""
    def has_object_permission(self, request, view, obj):
        # Lecture seule pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # Écriture seulement pour le propriétaire de la boutique
        return obj.boutique.utilisateur == request.user

# ============================================
# 📌 CLIENTS
# ============================================
class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Client.objects.filter(boutique__utilisateur=self.request.user)
    
    def perform_create(self, serializer):
        boutique = self.request.user.boutique
        serializer.save(boutique=boutique)

# ============================================
# 📌 COMMANDES
# ============================================
class CommandeListCreateView(generics.ListCreateAPIView):
    serializer_class = CommandeListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Commande.objects.filter(boutique__utilisateur=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommandeCreateSerializer
        return CommandeListSerializer
    
    def perform_create(self, serializer):
        boutique = self.request.user.boutique
        serializer.save(boutique=boutique)

class CommandeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [CommandePermission]

class CommandeStatutView(APIView):
    """Changer le statut d'une commande"""
    permission_classes = [CommandePermission]
    
    def patch(self, request, pk):
        commande = get_object_or_404(Commande, pk=pk)
        
        if commande.boutique.utilisateur != request.user:
            return Response(
                {'error': 'Non autorisé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        statut = request.data.get('statut')
        if statut:
            commande.statut = statut
            commande.save()
        
        serializer = CommandeSerializer(commande)
        return Response(serializer.data)

class CommandePubliqueView(APIView):
    """Créer une commande depuis la boutique publique"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, lien_site):
        from apps.accounts.models import Utilisateur
        from apps.boutiques.models import Boutique
        
        try:
            utilisateur = Utilisateur.objects.get(lien_site=lien_site, statut='actif')
            boutique = Boutique.objects.get(utilisateur=utilisateur, active=True)
        except:
            return Response(
                {'error': 'Boutique non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Créer ou récupérer le client
        client_data = request.data.get('client', {})
        client, created = Client.objects.get_or_create(
            boutique=boutique,
            telephone=client_data.get('telephone'),
            defaults={
                'nom': client_data.get('nom', 'Client'),
                'email': client_data.get('email', ''),
                'adresse': client_data.get('adresse', '')
            }
        )
        
        # Créer la commande
        commande_data = {
            'boutique': boutique.id,
            'client': client.id,
            'adresse_livraison': request.data.get('adresse_livraison'),
            'ville': request.data.get('ville'),
            'telephone_livraison': request.data.get('telephone_livraison'),
            'frais_livraison': request.data.get('frais_livraison', 0),
            'notes': request.data.get('notes', ''),
            'lignes': request.data.get('lignes', [])
        }
        
        serializer = CommandeCreateSerializer(data=commande_data)
        if serializer.is_valid():
            commande = serializer.save()
            return Response(
                CommandeSerializer(commande).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommandeStatsView(APIView):
    """Statistiques des commandes pour le vendeur"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        commandes = Commande.objects.filter(boutique__utilisateur=request.user)
        
        stats = {
            'total_commandes': commandes.count(),
            'en_attente': commandes.filter(statut='en_attente').count(),
            'validees': commandes.filter(statut='validee').count(),
            'livrees': commandes.filter(statut='livree').count(),
            'annulees': commandes.filter(statut='annulee').count(),
            'chiffre_affaires': sum(c.total_final for c in commandes.filter(statut__in=['livree', 'validee'])),
        }
        
        return Response(stats)