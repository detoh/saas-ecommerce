from rest_framework import serializers
from django.utils import timezone
from .models import Abonnement

class AbonnementSerializer(serializers.ModelSerializer):
    utilisateur_username = serializers.CharField(source='utilisateur.username', read_only=True)
    est_actif = serializers.ReadOnlyField()
    jours_restants = serializers.ReadOnlyField()
    est_expirable_bientot = serializers.ReadOnlyField()
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    plan_display = serializers.CharField(source='get_plan_display', read_only=True)
    
    class Meta:
        model = Abonnement
        fields = '__all__'
        read_only_fields = ('utilisateur', 'created_at', 'updated_at', 
                           'est_actif', 'jours_restants', 'est_expirable_bientot')

class AbonnementCreateSerializer(serializers.Serializer):
    plan = serializers.ChoiceField(choices=[
        ('basic', 'Basic - 10 000 FCFA/mois'),
        ('pro', 'Pro - 25 000 FCFA/mois'),
        ('premium', 'Premium - 50 000 FCFA/mois'),
    ])
    type_abo = serializers.ChoiceField(choices=[
        ('mensuel', 'Mensuel'),
        ('trimestriel', 'Trimestriel'),
        ('annuel', 'Annuel'),
    ])
    paiement_auto = serializers.BooleanField(default=False)

class AbonnementRenouvellementSerializer(serializers.Serializer):
    plan = serializers.ChoiceField(
        choices=[
            ('basic', 'Basic'),
            ('pro', 'Pro'),
            ('premium', 'Premium'),
        ],
        required=False
    )