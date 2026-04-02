import requests

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("📦 TEST GESTION DES PRODUITS")
print("=" * 60)

# Étape 1 : Connexion
print("\n🔐 Étape 1 : Connexion...")
login_data = {
    "username": "test_vendeur2",
    "password": "Password123!"
}
login_response = requests.post(f"{BASE_URL}/auth/connexion/", json=login_data)

if login_response.status_code != 200:
    print("❌ Échec de connexion. Utilisez un autre compte.")
    exit()

token = login_response.json().get('access')
headers = {"Authorization": f"Bearer {token}"}
print("✅ Connexion réussie !")

# Étape 2 : Créer un produit
print("\n📝 Étape 2 : Créer un produit...")
produit_data = {
    "nom": "Chaussures Nike Air",
    "description": "Chaussures de sport confortables et légères",
    "prix": "50000",
    "prix_promo": "45000",
    "stock": 20,
    "categorie": "chaussures",
    "is_visible": True
}

response = requests.post(f"{BASE_URL}/produits/", json=produit_data, headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 201:
    print("✅ Produit créé avec succès !")
    produit_id = response.json().get('id')
    print(f"ID Produit: {produit_id}")
    print(f"Nom: {response.json().get('nom')}")
    print(f"Prix: {response.json().get('prix')} FCFA")
    print(f"Prix Promo: {response.json().get('prix_promo')} FCFA")
else:
    print(f"❌ Échec: {response.json()}")
    # Si on a déjà des produits, on continue
    produit_id = 1

# Étape 3 : Lister les produits
print("\n📋 Étape 3 : Lister mes produits...")
response = requests.get(f"{BASE_URL}/produits/", headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    produits = response.json()
    print(f"✅ {len(produits)} produit(s) trouvé(s)")
    for p in produits[:3]:  # Afficher les 3 premiers
        print(f"   - {p['nom']}: {p['prix_actuel']} FCFA (Stock: {p['stock']})")

# Étape 4 : Recherche publique
print("\n🔍 Étape 4 : Recherche publique...")
response = requests.get(f"{BASE_URL}/produits/recherche/?q=chaussures")
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    produits = response.json()
    print(f"✅ {len(produits)} produit(s) trouvé(s) en recherche publique")

print("\n" + "=" * 60)
print("✅ TESTS PRODUITS TERMINÉS !")
print("=" * 60)