from django.urls import path
from .views import InscriptionView, ConnexionView, ProfilView

urlpatterns = [
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('connexion/', ConnexionView.as_view(), name='connexion'),
    path('profil/', ProfilView.as_view(), name='profil'),
]