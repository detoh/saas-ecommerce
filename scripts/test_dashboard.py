import requests

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("📈 TEST DASHBOARD VENDEUR & ADMIN")
print("=" * 60)

# Étape 1 : Connexion Vendeur
print("\n🔐 Étape 1 : Connexion Vendeur...")
login_data = {
    "username": "admin_test",
    "password": "Password123!"
}
login_response = requests.post(f"{BASE_URL}/auth/connexion/", json=login_data)

if login_response.status_code != 200:
    print("❌ Échec de connexion vendeur.")
    exit()

token_vendeur = login_response.json().get('access')
headers_vendeur = {"Authorization": f"Bearer {token_vendeur}"}
print("✅ Connexion vendeur réussie !")

# Étape 2 : Dashboard Vendeur
print("\n📊 Étape 2 : Dashboard Vendeur...")
response = requests.get(f"{BASE_URL}/dashboard/vendeur/", headers=headers_vendeur)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    dashboard = response.json()
    print("✅ Dashboard vendeur récupéré !")
    print(f"   Boutique: {dashboard.get('boutique', {}).get('nom')}")
    print(f"   Chiffre d'affaires (30j): {dashboard.get('chiffre_affaires', {}).get('30_jours')} FCFA")
    print(f"   Commandes totales: {dashboard.get('commandes', {}).get('total')}")
    print(f"   Produits: {dashboard.get('produits', {}).get('total')}")
    print(f"   Abonnement actif: {dashboard.get('abonnement', {}).get('actif')}")
else:
    print(f"❌ Échec: {response.text[:200]}")

# Étape 3 : Connexion Admin
print("\n🔐 Étape 3 : Connexion Admin...")
login_admin = {
    "username": "admin",  # Votre superutilisateur
    "password": "admin"   # Votre mot de passe admin
}
login_admin_response = requests.post(f"{BASE_URL}/auth/connexion/", json=login_admin)

if login_admin_response.status_code == 200:
    token_admin = login_admin_response.json().get('access')
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    print("✅ Connexion admin réussie !")
    
    # Étape 4 : Dashboard Admin
    print("\n📊 Étape 4 : Dashboard Admin...")
    response = requests.get(f"{BASE_URL}/dashboard/admin/", headers=headers_admin)
    print(f"Statut: {response.status_code}")
    
    if response.status_code == 200:
        dashboard = response.json()
        print("✅ Dashboard admin récupéré !")
        print(f"   Total vendeurs: {dashboard.get('statistiques_globales', {}).get('total_vendeurs')}")
        print(f"   Total boutiques: {dashboard.get('statistiques_globales', {}).get('total_boutiques')}")
        print(f"   Chiffre d'affaires global: {dashboard.get('statistiques_globales', {}).get('chiffre_affaires_global')} FCFA")
        print(f"   Revenus abonnements: {dashboard.get('abonnements', {}).get('revenus')} FCFA")
        print(f"   Taux succès paiements: {dashboard.get('paiements', {}).get('taux_success')}%")
    else:
        print(f"❌ Échec: {response.text[:200]}")
else:
    print("ℹ️ Admin non disponible (utilisez vos identifiants superutilisateur)")

print("\n" + "=" * 60)
print("✅ TESTS DASHBOARD TERMINÉS !")
print("=" * 60)