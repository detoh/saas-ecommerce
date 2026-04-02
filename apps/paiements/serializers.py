from rest_framework import serializers
from .models import Paiement

class PaiementSerializer(serializers.ModelSerializer):
    commande_reference = serializers.CharField(source='commande.reference', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    methode_display = serializers.CharField(source='get_methode_display', read_only=True)
    
    class Meta:
        model = Paiement
        fields = '__all__'
        read_only_fields = ('commande', 'reference_interne', 'date_paiement', 
                           'date_validation', 'date_echec', 'operateur_response')

class PaiementInitSerializer(serializers.Serializer):
    commande_id = serializers.IntegerField()
    methode = serializers.ChoiceField(choices=[
        ('orange_money', 'Orange Money'),
        ('wave', 'Wave'),
        ('mtn_money', 'MTN Money'),
        ('moov_money', 'Moov Money'),
    ])
    telephone = serializers.CharField(max_length=20)

class PaiementCallbackSerializer(serializers.Serializer):
    transaction_id = serializers.CharField()
    statut = serializers.CharField()
    montant = serializers.DecimalField(max_digits=10, decimal_places=2)
    reference = serializers.CharField()