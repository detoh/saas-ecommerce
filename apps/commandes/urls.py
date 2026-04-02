from django.urls import path

urlpatterns = [
    # Les routes produits seront ajoutées ici
]
from django.urls import path
from .views import (
    ClientListCreateView, CommandeListCreateView, CommandeDetailView,
    CommandeStatutView, CommandePubliqueView, CommandeStatsView
)

urlpatterns = [
    path('clients/', ClientListCreateView.as_view(), name='client-list'),
    path('', CommandeListCreateView.as_view(), name='commande-list'),
    path('<int:pk>/', CommandeDetailView.as_view(), name='commande-detail'),
    path('<int:pk>/statut/', CommandeStatutView.as_view(), name='commande-statut'),
    path('publique/<str:lien_site>/', CommandePubliqueView.as_view(), name='commande-publique'),
    path('stats/', CommandeStatsView.as_view(), name='commande-stats'),
]