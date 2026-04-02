from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Abonnement
from .serializers import (
    AbonnementSerializer, AbonnementCreateSerializer,
    AbonnementRenouvellementSerializer
)

class AbonnementPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.utilisateur == request.user

class AbonnementListView(generics.ListAPIView):
    serializer_class = AbonnementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Abonnement.objects.filter(utilisateur=self.request.user)

class AbonnementDetailView(generics.RetrieveAPIView):
    serializer_class = AbonnementSerializer
    permission_classes = [AbonnementPermission]
    
    def get_queryset(self):
        return Abonnement.objects.filter(utilisateur=self.request.user)

class AbonnementActifView(APIView):
    """Récupérer l'abonnement actif de l'utilisateur"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        abonnement = Abonnement.objects.filter(
            utilisateur=request.user,
            statut='actif',
            date_fin__gte=timezone.now().date()
        ).first()
        
        if abonnement:
            return Response(AbonnementSerializer(abonnement).data)
        else:
            return Response(
                {'message': 'Aucun abonnement actif'},
                status=status.HTTP_404_NOT_FOUND
            )

class AbonnementCreateView(APIView):
    """Créer un nouvel abonnement"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = AbonnementCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        plan = serializer.validated_data['plan']
        type_abo = serializer.validated_data['type_abo']
        
        # Définir les prix
        prix_plan = {
            'basic': 10000,
            'pro': 25000,
            'premium': 50000,
        }
        
        prix = prix_plan.get(plan, 10000)
        
        # Ajuster selon le type
        if type_abo == 'trimestriel':
            prix = prix * 3 * 0.9  # 10% de réduction
        elif type_abo == 'annuel':
            prix = prix * 12 * 0.8  # 20% de réduction
        
        # Créer l'abonnement
        abonnement = Abonnement.objects.create(
            utilisateur=request.user,
            plan=plan,
            type_abo=type_abo,
            prix=prix,
            date_debut=timezone.now().date(),
            statut='impaye'  # En attente de paiement
        )
        
        return Response({
            'abonnement': AbonnementSerializer(abonnement).data,
            'message': 'Abonnement créé. Veuillez procéder au paiement.',
            'montant_a_payer': prix
        }, status=status.HTTP_201_CREATED)

class AbonnementRenouvellementView(APIView):
    """Renouveler un abonnement"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = AbonnementRenouvellementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Récupérer l'abonnement actif
        abonnement = Abonnement.objects.filter(
            utilisateur=request.user,
            statut='actif'
        ).first()
        
        if not abonnement:
            return Response(
                {'error': 'Aucun abonnement actif à renouveler'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Renouveler
        plan = serializer.validated_data.get('plan', abonnement.plan)
        abonnement.renouveler(plan)
        
        return Response({
            'abonnement': AbonnementSerializer(abonnement).data,
            'message': 'Abonnement renouvelé avec succès'
        })

class AbonnementStatsView(APIView):
    """Statistiques d'abonnement pour le vendeur"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        abonnements = Abonnement.objects.filter(utilisateur=request.user)
        abonnement_actif = abonnements.filter(
            statut='actif',
            date_fin__gte=timezone.now().date()
        ).first()
        
        stats = {
            'total_abonnements': abonnements.count(),
            'abonnement_actif': AbonnementSerializer(abonnement_actif).data if abonnement_actif else None,
            'jours_restants': abonnement_actif.jours_restants if abonnement_actif else 0,
            'expirable_bientot': abonnement_actif.est_expirable_bientot if abonnement_actif else False,
            'historique': AbonnementSerializer(abonnements, many=True).data[:5]
        }
        
        return Response(stats)

class VerificationAbonnementView(APIView):
    """Vérifie si l'utilisateur a un abonnement actif (pour middleware)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        abonnement = Abonnement.objects.filter(
            utilisateur=request.user,
            statut='actif',
            date_fin__gte=timezone.now().date()
        ).first()
        
        return Response({
            'actif': abonnement is not None,
            'plan': abonnement.plan if abonnement else None,
            'date_fin': abonnement.date_fin if abonnement else None,
            'jours_restants': abonnement.jours_restants if abonnement else 0
        })