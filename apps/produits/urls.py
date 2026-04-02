from django.urls import path
from .views import (
    ProduitListCreateView, ProduitDetailView, ProduitPubliqueView,
    ProduitRechercheView, ProduitImageUploadView, ProduitImageDeleteView,
    CategorieListCreateView, CategorieDetailView, CategoriePubliqueView
)

urlpatterns = [
    path('', ProduitListCreateView.as_view(), name='produit-list'),
    path('<int:pk>/', ProduitDetailView.as_view(), name='produit-detail'),
    path('boutique/<str:lien_site>/', ProduitPubliqueView.as_view(), name='produit-publique'),
    path('recherche/', ProduitRechercheView.as_view(), name='produit-recherche'),
    path('<int:produit_id>/images/', ProduitImageUploadView.as_view(), name='produit-images-upload'),
    path('<int:produit_id>/images/<int:image_index>/', ProduitImageDeleteView.as_view(), name='produit-images-delete'),
    path('categories/', CategorieListCreateView.as_view(), name='categorie-list'),
    path('categories/<int:pk>/', CategorieDetailView.as_view(), name='categorie-detail'),
    path('categories-publiques/<str:lien_site>/', CategoriePubliqueView.as_view(), name='categorie-publique'),
]