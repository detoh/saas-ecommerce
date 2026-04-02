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
print("📝 CRÉATION UTILISATEUR DE TEST")
print("=" * 60)

# Vérifier si l'utilisateur existe déjà
if Utilisateur.objects.filter(username='admin_test').exists():
    print("\nℹ️ L'utilisateur 'admin_test' existe déjà")
    user = Utilisateur.objects.get(username='admin_test')
else:
    # Créer l'utilisateur
    user = Utilisateur.objects.create_user(
        username='admin_test',
        email='admin@saas.com',
        password='Password123!',
        first_name='Admin',
        last_name='Test',
        telephone='07070707',
        lien_site='admin-boutique',
        statut='actif'
    )
    print("\n✅ Utilisateur créé avec succès !")

print(f"\n📋 Informations de connexion :")
print(f"   Username: admin_test")
print(f"   Mot de passe: Password123!")
print(f"   Email: {user.email}")
print(f"   Statut: {user.statut}")

print("\n" + "=" * 60)