import os
import sys
import django

# ============================================
# AJOUTER LE CHEMIN DU PROJET À PYTHONPATH
# ============================================
# Ceci permet à Python de trouver le module 'config'
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Définir le module de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialiser Django
django.setup()

# ============================================
# CRÉATION UTILISATEUR
# ============================================
from apps.accounts.models import Utilisateur

print("=" * 60)
print("📝 CRÉATION UTILISATEUR ")
print("=" * 60)

# Vérifier si l'utilisateur existe déjà
if Utilisateur.objects.filter(username='pale').exists():
    print("\nℹ️ L'utilisateur 'pale' existe déjà")
    user = Utilisateur.objects.get(username='pale')
else:
    # Créer l'utilisateur
    user = Utilisateur.objects.create_user(
        username='pale',
        email='palebato@saas.com',
        password='Bato#2026',
        first_name='Pale',
        last_name='Frederick',
        telephone='07070707',
        lien_site='pale-boutique',
        statut='actif'
    )
    print("\n✅ Utilisateur créé avec succès !")

print(f"\n📋 Informations de connexion :")
print(f"   Username: pale")
print(f"   Mot de passe: Bato#2026")
print(f"   Email: {user.email}")
print(f"   Statut: {user.statut}")

print("\n" + "=" * 60)