from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta

class DashboardVendeurView(APIView):
    """Tableau de bord complet pour le vendeur"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        from apps.boutiques.models import Boutique
        from apps.produits.models import Produit
        from apps.commandes.models import Commande
        from apps.paiements.models import Paiement
        from apps.abonnements.models import Abonnement
        
        # Vérifier que l'utilisateur a une boutique
        try:
            boutique = request.user.boutique
        except:
            return Response(
                {'error': 'Vous n\'avez pas de boutique'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Statistiques générales
        commandes = Commande.objects.filter(boutique=boutique)
        produits = Produit.objects.filter(boutique=boutique)
        paiements = Paiement.objects.filter(commande__boutique=boutique)
        
        # Période (30 derniers jours)
        date_30_jours = timezone.now() - timedelta(days=30)
        commandes_recentes = commandes.filter(date_commande__gte=date_30_jours)
        
        # Calculs
        chiffre_affaires = sum(
            c.total_final for c in commandes.filter(statut__in=['livree', 'validee'])
        )
        chiffre_affaires_30j = sum(
            c.total_final for c in commandes_recentes.filter(statut__in=['livree', 'validee'])
        )
        
        commandes_par_statut = {
            'en_attente': commandes.filter(statut='en_attente').count(),
            'validees': commandes.filter(statut='validee').count(),
            'en_preparation': commandes.filter(statut='en_preparation').count(),
            'expediees': commandes.filter(statut='expediee').count(),
            'livrees': commandes.filter(statut='livree').count(),
            'annulees': commandes.filter(statut='annulee').count(),
        }
        
        # Produits
        produits_stats = {
            'total': produits.count(),
            'en_stock': produits.filter(stock__gt=0).count(),
            'rupture': produits.filter(stock=0).count(),
            'visibles': produits.filter(is_visible=True).count(),
        }
        
        # Abonnement
        abonnement = Abonnement.objects.filter(
            utilisateur=request.user,
            statut='actif',
            date_fin__gte=timezone.now().date()
        ).first()
        
        # Paiements récents
        paiements_recents = paiements.order_by('-date_paiement')[:5]
        
        # Commandes récentes
        commandes_recentes_list = commandes.order_by('-date_commande')[:5]
        
        return Response({
            'boutique': {
                'nom': boutique.nom_boutique,
                'theme': boutique.theme,
                'active': boutique.active,
                'url': boutique.url_boutique
            },
            'chiffre_affaires': {
                'total': float(chiffre_affaires),
                '30_jours': float(chiffre_affaires_30j),
                'devise': boutique.devise
            },
            'commandes': {
                'total': commandes.count(),
                'par_statut': commandes_par_statut,
                'recentes': [
                    {
                        'id': c.id,
                        'reference': c.reference,
                        'client': c.client.nom,
                        'total': float(c.total_final),
                        'statut': c.statut,
                        'date': c.date_commande.isoformat()
                    }
                    for c in commandes_recentes_list
                ]
            },
            'produits': produits_stats,
            'abonnement': {
                'actif': abonnement is not None,
                'plan': abonnement.plan if abonnement else None,
                'date_fin': abonnement.date_fin.isoformat() if abonnement else None,
                'jours_restants': abonnement.jours_restants if abonnement else 0
            },
            'paiements': [
                {
                    'reference': p.reference_interne,
                    'montant': float(p.montant),
                    'methode': p.methode,
                    'statut': p.statut,
                    'date': p.date_paiement.isoformat()
                }
                for p in paiements_recents
            ]
        })
class DashboardAdminView(APIView):
    """Tableau de bord pour l'administrateur principal"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        from apps.accounts.models import Utilisateur
        from apps.boutiques.models import Boutique
        from apps.commandes.models import Commande
        from apps.paiements.models import Paiement
        from apps.abonnements.models import Abonnement
        
        # Vérifier que c'est un admin
        if not request.user.is_staff:
            return Response(
                {'error': 'Accès réservé aux administrateurs'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Statistiques globales
        total_vendeurs = Utilisateur.objects.filter(statut='actif').count()
        total_boutiques = Boutique.objects.count()
        total_boutiques_actives = Boutique.objects.filter(
            utilisateur__statut='actif'
        ).count()
        
        # Commandes
        commandes = Commande.objects.all()
        total_commandes = commandes.count()
        chiffre_affaires_global = sum(
            c.total_final for c in commandes.filter(statut__in=['livree', 'validee'])
        )
        
        # Abonnements
        abonnements = Abonnement.objects.all()
        abonnements_actifs = abonnements.filter(
            statut='actif',
            date_fin__gte=timezone.now().date()
        ).count()
        revenus_abonnements = sum(
            a.prix for a in abonnements.filter(statut='actif')
        )
        
        # Paiements
        paiements = Paiement.objects.all()
        paiements_success = paiements.filter(statut='success').count()
        paiements_pending = paiements.filter(statut='pending').count()
        paiements_failed = paiements.filter(statut='failed').count()
        
        # Vendeurs par statut
        vendeurs_stats = {
            'actifs': Utilisateur.objects.filter(statut='actif').count(),
            'suspendus': Utilisateur.objects.filter(statut='suspendu').count(),
            'en_attente': Utilisateur.objects.filter(statut='en_attente').count(),
        }
        
        # Top 5 boutiques par chiffre d'affaires
        top_boutiques = []
        for boutique in Boutique.objects.all()[:10]:
            ca_boutique = sum(
                c.total_final for c in Commande.objects.filter(
                    boutique=boutique,
                    statut__in=['livree', 'validee']
                )
            )
            top_boutiques.append({
                'nom': boutique.nom_boutique,
                'vendeur': boutique.utilisateur.username,
                'chiffre_affaires': float(ca_boutique)
            })
        top_boutiques.sort(key=lambda x: x['chiffre_affaires'], reverse=True)
        
        # Évolution (30 derniers jours)
        date_30_jours = timezone.now() - timedelta(days=30)
        nouvelles_inscriptions = Utilisateur.objects.filter(
            date_creation__gte=date_30_jours
        ).count()
        nouvelles_commandes = commandes.filter(
            date_commande__gte=date_30_jours
        ).count()
        nouveaux_abonnements = abonnements.filter(
            created_at__gte=date_30_jours
        ).count()
        
        return Response({
            'statistiques_globales': {
                'total_vendeurs': total_vendeurs,
                'total_boutiques': total_boutiques,
                'boutiques_actives': total_boutiques_actives,
                'total_commandes': total_commandes,
                'chiffre_affaires_global': float(chiffre_affaires_global),
            },
            'abonnements': {
                'total': abonnements.count(),
                'actifs': abonnements_actifs,
                'revenus': float(revenus_abonnements)
            },
            'paiements': {
                'total': paiements.count(),
                'success': paiements_success,
                'pending': paiements_pending,
                'failed': paiements_failed,
                'taux_success': round((paiements_success / paiements.count() * 100) if paiements.count() > 0 else 0, 2)
            },
            'vendeurs': vendeurs_stats,
            'top_boutiques': top_boutiques[:5],
            'evolution_30j': {
                'nouvelles_inscriptions': nouvelles_inscriptions,
                'nouvelles_commandes': nouvelles_commandes,
                'nouveaux_abonnements': nouveaux_abonnements
            }
        })
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

def accueil(request):
    """Page d'accueil simple"""
    return render(request, 'accueil.html', {})