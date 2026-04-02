from rest_framework import serializers
from .models import Boutique

class BoutiqueSerializer(serializers.ModelSerializer):
    proprietaire = serializers.CharField(source='utilisateur.username', read_only=True)
    email_proprietaire = serializers.EmailField(source='utilisateur.email', read_only=True)
    active = serializers.ReadOnlyField()
    url_boutique = serializers.ReadOnlyField()
    
    class Meta:
        model = Boutique
        fields = '__all__'
        read_only_fields = ('utilisateur', 'created_at', 'updated_at', 'active', 'url_boutique')

class BoutiqueListSerializer(serializers.ModelSerializer):
    proprietaire = serializers.CharField(source='utilisateur.username', read_only=True)
    active = serializers.ReadOnlyField()
    
    class Meta:
        model = Boutique
        fields = ('id', 'nom_boutique', 'logo', 'theme', 'devise', 'proprietaire', 'active', 'created_at')