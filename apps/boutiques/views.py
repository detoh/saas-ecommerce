from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Boutique
from .serializers import BoutiqueSerializer, BoutiqueListSerializer
from apps.accounts.models import Utilisateur

class BoutiquePermission(permissions.BasePermission):
    """Permission personnalisée pour les boutiques"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.utilisateur == request.user

class BoutiqueListCreateView(generics.ListCreateAPIView):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Boutique.objects.filter(utilisateur=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

class BoutiqueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer
    permission_classes = [BoutiquePermission]

class MaBoutiqueView(APIView):
    """Vue pour gérer sa propre boutique"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            boutique = Boutique.objects.get(utilisateur=request.user)
            serializer = BoutiqueSerializer(boutique)
            return Response(serializer.data)
        except Boutique.DoesNotExist:
            return Response(
                {'message': 'Vous n\'avez pas encore de boutique'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def post(self, request):
        if hasattr(request.user, 'boutique'):
            return Response(
                {'error': 'Vous avez déjà une boutique'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = BoutiqueSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        boutique = serializer.save(utilisateur=request.user)
        return Response(BoutiqueSerializer(boutique).data, status=status.HTTP_201_CREATED)

class BoutiquePubliqueView(APIView):
    """Vue publique pour afficher une boutique par lien_site"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, lien_site):
        try:
            utilisateur = Utilisateur.objects.get(lien_site=lien_site, statut='actif')
            boutique = Boutique.objects.get(utilisateur=utilisateur)
            
            if not boutique.active:
                return Response(
                    {'error': 'Cette boutique est temporairement fermée'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = BoutiqueSerializer(boutique)
            return Response(serializer.data)
        except Utilisateur.DoesNotExist:
            return Response(
                {'error': 'Boutique non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Boutique.DoesNotExist:
            return Response(
                {'error': 'Boutique non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )

class BoutiquePubliqueDetailView(APIView):
    """Vue publique pour afficher une boutique complète"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, lien_site):
        try:
            from apps.produits.models import Produit, Categorie
            from apps.boutiques.serializers import ProduitListSerializer, CategorieListSerializer
            
            utilisateur = Utilisateur.objects.get(lien_site=lien_site, statut='actif')
            boutique = Boutique.objects.get(utilisateur=utilisateur, active=True)
            
            categories = Categorie.objects.filter(
                boutique=boutique,
                is_active=True
            )
            
            produits = Produit.objects.filter(
                boutique=boutique,
                is_visible=True
            ).order_by('-created_at')[:12]
            
            return Response({
                'boutique': BoutiqueSerializer(boutique).data,
                'categories': CategorieListSerializer(categories, many=True).data,
                'produits': ProduitListSerializer(produits, many=True).data,
                'total_produits': Produit.objects.filter(boutique=boutique, is_visible=True).count(),
            })
        except Utilisateur.DoesNotExist:
            return Response(
                {'error': 'Boutique non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Boutique.DoesNotExist:
            return Response(
                {'error': 'Boutique non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )

class ProduitsParCategorieView(APIView):
    """Vue publique pour afficher les produits d'une catégorie"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, lien_site, categorie_slug):
        try:
            from apps.produits.models import Produit, Categorie
            from apps.boutiques.serializers import ProduitListSerializer, CategorieListSerializer
            
            utilisateur = Utilisateur.objects.get(lien_site=lien_site, statut='actif')
            boutique = Boutique.objects.get(utilisateur=utilisateur, active=True)
            categorie = Categorie.objects.get(boutique=boutique, slug=categorie_slug, is_active=True)
            
            produits = Produit.objects.filter(
                boutique=boutique,
                categorie=categorie,
                is_visible=True
            )
            
            return Response({
                'boutique': BoutiqueSerializer(boutique).data,
                'categorie': CategorieListSerializer(categorie).data,
                'produits': ProduitListSerializer(produits, many=True).data,
            })
        except:
            return Response(
                {'error': 'Catégorie non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )