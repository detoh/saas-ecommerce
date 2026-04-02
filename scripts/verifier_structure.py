import os

apps = ['core', 'accounts', 'boutiques', 'produits', 'commandes', 'paiements', 'abonnements', 'api']

print("🔍 Vérification de la structure...")
print("=" * 50)

for app in apps:
    chemin = f"apps\\{app}"
    init_file = f"apps\\{app}\\__init__.py"
    apps_file = f"apps\\{app}\\apps.py"
    
    print(f"\n📁 {app}:")
    print(f"   Dossier: {'✅' if os.path.exists(chemin) else '❌'}")
    print(f"   __init__.py: {'✅' if os.path.exists(init_file) else '❌'}")
    print(f"   apps.py: {'✅' if os.path.exists(apps_file) else '❌'}")

print("\n" + "=" * 50)
print("✅ Vérification terminée !")