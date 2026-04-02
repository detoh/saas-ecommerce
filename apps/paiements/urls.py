from django.urls import path

urlpatterns = [
    # Les routes boutiques seront ajoutées ici
    
]

from django.urls import path
from .views import (
    PaiementInitView, PaiementDetailView, PaiementStatusView,
    PaiementPublicView
)

urlpatterns = [
    path('initier/', PaiementInitView.as_view(), name='paiement-init'),
    path('<int:pk>/', PaiementDetailView.as_view(), name='paiement-detail'),
    path('<int:pk>/statut/', PaiementStatusView.as_view(), name='paiement-statut'),
    path('publique/<str:lien_site>/<int:commande_id>/', PaiementPublicView.as_view(), name='paiement-public'),
]