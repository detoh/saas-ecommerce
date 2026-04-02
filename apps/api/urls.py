from django.urls import path, include


urlpatterns = [
    path('auth/', include('apps.accounts.urls')),
    path('boutiques/', include('apps.boutiques.urls')),
    path('produits/', include('apps.produits.urls')),
    path('commandes/', include('apps.commandes.urls')),
    path('paiements/', include('apps.paiements.urls')),
    path('abonnements/', include('apps.abonnements.urls')),  # ← IMPORTANT !
    path('dashboard/', include('apps.core.urls')),  # ← Ajouter ceci 
]
