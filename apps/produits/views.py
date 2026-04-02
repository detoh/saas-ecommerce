from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Produit, Categorie
from .serializers import ProduitSerializer, ProduitListSerializer, CategorieSerializer, CategorieListSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.core.files.storage import default_storage

class ProduitListCreateView(generics.ListCreateAPIView):
    serializer_class = ProduitListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Produit.objects.filter(boutique__utilisateur=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        boutique = self.request.user.boutique
        serializer.save(boutique=boutique)

class ProduitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProduitSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Produit.objects.filter(boutique__utilisateur=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ProduitPubliqueView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, lien_site):
        try:
            from apps.accounts.models import Utilisateur
            from apps.boutiques.models import Boutique
            
            utilisateur = Utilisateur.objects.get(lien_site=lien_site, statut='actif')
            boutique = Boutique.objects.get(utilisateur=utilisateur, active=True)
            
            produits = Produit.objects.filter(boutique=boutique, is_visible=True)
            serializer = ProduitListSerializer(produits, many=True, context={'request': request})
            return Response(serializer.data)
        except:
            return Response({'error': 'Boutique non trouvée'}, status=status.HTTP_404_NOT_FOUND)

class ProduitRechercheView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        categorie = request.query_params.get('categorie', '')
        
        produits = Produit.objects.filter(is_visible=True)
        
        if query:
            produits = produits.filter(nom__icontains=query)
        if categorie:
            produits = produits.filter(categorie__slug=categorie)
        
        serializer = ProduitListSerializer(produits, many=True, context={'request': request})
        return Response(serializer.data)

class ProduitImageUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, produit_id):
        try:
            produit = Produit.objects.get(id=produit_id, boutique__utilisateur=request.user)
            images = request.FILES.getlist('images')
            
            if len(images) > 3:
                return Response({'error': 'Maximum 3 images supplémentaires'}, status=status.HTTP_400_BAD_REQUEST)
            
            urls = []
            for image in images:
                path = default_storage.save(f'produits/{image.name}', image)
                url = f'{settings.MEDIA_URL}{path}'
                urls.append(url)
            
            existing_images = produit.images_supplementaires or []
            produit.images_supplementaires = existing_images + urls
            produit.save()
            
            return Response({'message': 'Images uploadées', 'images': produit.images_supplementaires})
        except Produit.DoesNotExist:
            return Response({'error': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)

class ProduitImageDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, produit_id, image_index):
        try:
            produit = Produit.objects.get(id=produit_id, boutique__utilisateur=request.user)
            
            if not produit.images_supplementaires or int(image_index) >= len(produit.images_supplementaires):
                return Response({'error': 'Image non trouvée'}, status=status.HTTP_404_NOT_FOUND)
            
            produit.images_supplementaires.pop(int(image_index))
            produit.save()
            
            return Response({'message': 'Image supprimée'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CategorieListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorieListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Categorie.objects.filter(boutique__utilisateur=self.request.user)
    
    def perform_create(self, serializer):
        boutique = self.request.user.boutique
        serializer.save(boutique=boutique)

class CategorieDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Categorie.objects.filter(boutique__utilisateur=self.request.user)

class CategoriePubliqueView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, lien_site):
        try:
            from apps.accounts.models import Utilisateur
            from apps.boutiques.models import Boutique
            
            utilisateur = Utilisateur.objects.get(lien_site=lien_site, statut='actif')
            boutique = Boutique.objects.get(utilisateur=utilisateur, active=True)
            
            categories = Categorie.objects.filter(boutique=boutique, is_active=True)
            serializer = CategorieListSerializer(categories, many=True)
            return Response(serializer.data)
        except:
            return Response({'error': 'Boutique non trouvée'}, status=status.HTTP_404_NOT_FOUND)