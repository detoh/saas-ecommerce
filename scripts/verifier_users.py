import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import Utilisateur

print("=" * 60)
print("👤 UTILISATEURS ENREGISTRÉS")
print("=" * 60)

users = Utilisateur.objects.all()

if users.count() == 0:
    print("\n❌ Aucun utilisateur dans la base de données !")
    print("\n📝 Créez un utilisateur avec :")
    print("   python scripts\test_auth.py")
else:
    print(f"\n✅ {users.count()} utilisateur(s) trouvé(s) :\n")
    for user in users:
        print(f"   - Username: {user.username}")
        print(f"     Email: {user.email}")
        print(f"     Statut: {user.statut}")
        print(f"     Lien site: {user.lien_site}")
        print()

print("=" * 60)