from rest_framework import serializers
from .models import Client, Commande, LigneCommande

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('boutique', 'created_at')

class LigneCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LigneCommande
        fields = '__all__'
        read_only_fields = ('sous_total',)

class LigneCommandeCreateSerializer(serializers.Serializer):
    produit_id = serializers.IntegerField()
    quantite = serializers.IntegerField(min_value=1)

class CommandeSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom', read_only=True)
    client_telephone = serializers.CharField(source='client.telephone', read_only=True)
    lignes = LigneCommandeSerializer(many=True, read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = Commande
        fields = '__all__'
        read_only_fields = ('reference', 'date_commande', 'total', 'total_final')

class CommandeCreateSerializer(serializers.ModelSerializer):
    lignes = LigneCommandeCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Commande
        fields = ('client', 'adresse_livraison', 'ville', 'telephone_livraison', 
                  'frais_livraison', 'notes', 'lignes')
    
    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes')
        commande = Commande.objects.create(**validated_data)
        
        for ligne_data in lignes_data:
            produit_id = ligne_data.pop('produit_id')
            from apps.produits.models import Produit
            produit = Produit.objects.get(id=produit_id)
            
            LigneCommande.objects.create(
                commande=commande,
                produit=produit,
                nom_produit=produit.nom,
                prix_unitaire=produit.prix_actuel,
                **ligne_data
            )
            
            # Décrémenter le stock
            produit.stock -= ligne_data['quantite']
            produit.save()
        
        commande.calculer_total()
        return commande

class CommandeListSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.nom', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    nombre_articles = serializers.SerializerMethodField()
    
    class Meta:
        model = Commande
        fields = ('id', 'reference', 'client_nom', 'statut', 'statut_display', 
                  'total_final', 'nombre_articles', 'date_commande', 'ville')
    
    def get_nombre_articles(self, obj):
        return obj.lignes.count()