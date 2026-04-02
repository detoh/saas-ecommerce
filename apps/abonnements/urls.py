
from django.urls import path

from .views import (
    AbonnementListView, AbonnementDetailView, AbonnementActifView,
    AbonnementCreateView, AbonnementRenouvellementView,
    AbonnementStatsView, VerificationAbonnementView
)

urlpatterns = [
    path('', AbonnementListView.as_view(), name='abonnement-list'),
    path('actif/', AbonnementActifView.as_view(), name='abonnement-actif'),
    path('creer/', AbonnementCreateView.as_view(), name='abonnement-creer'),
    path('renouveler/', AbonnementRenouvellementView.as_view(), name='abonnement-renouveler'),
    path('stats/', AbonnementStatsView.as_view(), name='abonnement-stats'),
    path('verification/', VerificationAbonnementView.as_view(), name='abonnement-verification'),
    path('<int:pk>/', AbonnementDetailView.as_view(), name='abonnement-detail'),
]