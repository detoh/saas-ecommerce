from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Paiement
from .serializers import PaiementSerializer, PaiementInitSerializer
from .services import MobileMoneyService
from apps.commandes.models import Commande

class PaiementPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.commande.boutique.utilisateur == request.user

class PaiementInitView(APIView):
    """Initier un paiement pour une commande"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PaiementInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        commande_id = serializer.validated_data['commande_id']
        methode = serializer.validated_data['methode']
        telephone = serializer.validated_data['telephone']
        
        # Récupérer la commande
        try:
            commande = Commande.objects.get(
                id=commande_id,
                boutique__utilisateur=request.user
            )
        except Commande.DoesNotExist:
            return Response(
                {'error': 'Commande non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier si un paiement existe déjà
        if hasattr(commande, 'paiement'):
            return Response(
                {'error': 'Un paiement existe déjà pour cette commande'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer le paiement
        paiement = Paiement.objects.create(
            commande=commande,
            montant=commande.total_final,
            methode=methode,
            telephone_paiement=telephone
        )
        
        # Initier le paiement avec l'opérateur
        result = MobileMoneyService.initier_paiement(
            paiement, 
            telephone, 
            commande.total_final
        )
        
        if result['success']:
            return Response({
                'paiement': PaiementSerializer(paiement).data,
                'message': result['message']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['message']
            }, status=status.HTTP_400_BAD_REQUEST)

class PaiementDetailView(APIView):
    """Voir le détail d'un paiement"""
    permission_classes = [PaiementPermission]
    
    def get(self, request, pk):
        paiement = get_object_or_404(Paiement, pk=pk)
        serializer = PaiementSerializer(paiement)
        return Response(serializer.data)

class PaiementStatusView(APIView):
    """Vérifier le statut d'un paiement"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        try:
            paiement = Paiement.objects.get(
                pk=pk,
                commande__boutique__utilisateur=request.user
            )
            return Response({
                'reference': paiement.reference_interne,
                'statut': paiement.statut,
                'statut_display': paiement.get_statut_display(),
                'montant': paiement.montant,
                'methode': paiement.get_methode_display(),
                'date_paiement': paiement.date_paiement,
                'date_validation': paiement.date_validation
            })
        except Paiement.DoesNotExist:
            return Response(
                {'error': 'Paiement non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

class PaiementPublicView(APIView):
    """Initier un paiement depuis la boutique publique"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, lien_site, commande_id):
        from apps.accounts.models import Utilisateur
        from apps.boutiques.models import Boutique
        
        try:
            utilisateur = Utilisateur.objects.get(lien_site=lien_site, statut='actif')
            boutique = Boutique.objects.get(utilisateur=utilisateur, active=True)
            commande = Commande.objects.get(id=commande_id, boutique=boutique)
        except:
            return Response(
                {'error': 'Commande non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        methode = request.data.get('methode')
        telephone = request.data.get('telephone')
        
        if not methode or not telephone:
            return Response(
                {'error': 'Méthode et téléphone requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer le paiement
        paiement = Paiement.objects.create(
            commande=commande,
            montant=commande.total_final,
            methode=methode,
            telephone_paiement=telephone
        )
        
        # Initier le paiement
        result = MobileMoneyService.initier_paiement(
            paiement, 
            telephone, 
            commande.total_final
        )
        
        if result['success']:
            return Response({
                'paiement': PaiementSerializer(paiement).data,
                'message': result['message']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['message']
            }, status=status.HTTP_400_BAD_REQUEST)