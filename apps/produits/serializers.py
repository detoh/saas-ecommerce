from rest_framework import serializers
from .models import Produit, Categorie

class CategorieSerializer(serializers.ModelSerializer):
    nombre_produits = serializers.ReadOnlyField()
    
    class Meta:
        model = Categorie
        fields = '__all__'
        read_only_fields = ('boutique', 'slug', 'created_at', 'updated_at')

class CategorieListSerializer(serializers.ModelSerializer):
    nombre_produits = serializers.ReadOnlyField()
    
    class Meta:
        model = Categorie
        fields = ('id', 'nom', 'slug', 'description', 'image', 'nombre_produits', 'is_active', 'created_at')

class ProduitSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    prix_actuel = serializers.ReadOnlyField()
    en_stock = serializers.ReadOnlyField()
    toutes_les_images = serializers.ReadOnlyField()
    
    class Meta:
        model = Produit
        fields = '__all__'
        read_only_fields = ('boutique', 'created_at', 'updated_at', 'prix_actuel', 'en_stock', 'toutes_les_images')
    
    def create(self, validated_data):
        boutique = self.context['request'].user.boutique
        validated_data['boutique'] = boutique
        return super().create(validated_data)

class ProduitListSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    prix_actuel = serializers.ReadOnlyField()
    en_stock = serializers.ReadOnlyField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Produit
        fields = ('id', 'nom', 'description', 'prix', 'prix_promo', 'prix_actuel', 
                  'stock', 'en_stock', 'image', 'image_url', 'images_supplementaires',
                  'categorie', 'categorie_nom', 'is_visible', 'created_at')
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None