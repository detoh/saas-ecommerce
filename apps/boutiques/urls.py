from django.urls import path

urlpatterns = [
    # Les routes boutiques seront ajoutées ici
]
from django.urls import path
from .views import BoutiqueListCreateView, BoutiqueDetailView, MaBoutiqueView, BoutiquePubliqueView

urlpatterns = [
    path('', BoutiqueListCreateView.as_view(), name='boutique-list'),
    path('ma-boutique/', MaBoutiqueView.as_view(), name='ma-boutique'),
    path('<int:pk>/', BoutiqueDetailView.as_view(), name='boutique-detail'),
    path('publique/<str:lien_site>/', BoutiquePubliqueView.as_view(), name='boutique-publique'),
]

from .views import (
    BoutiqueListCreateView, BoutiqueDetailView, MaBoutiqueView,
    BoutiquePubliqueView, BoutiquePubliqueDetailView, ProduitsParCategorieView
)

urlpatterns = [
    path('', BoutiqueListCreateView.as_view(), name='boutique-list'),
    path('ma-boutique/', MaBoutiqueView.as_view(), name='ma-boutique'),
    path('<int:pk>/', BoutiqueDetailView.as_view(), name='boutique-detail'),
    path('publique/<str:lien_site>/', BoutiquePubliqueView.as_view(), name='boutique-publique'),
    
    # Site public complet
    path('site/<str:lien_site>/', BoutiquePubliqueDetailView.as_view(), name='boutique-site'),
    path('site/<str:lien_site>/categorie/<str:categorie_slug>/', ProduitsParCategorieView.as_view(), name='produits-categorie'),
]