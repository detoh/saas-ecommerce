import requests

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("🛒 TEST GESTION DES COMMANDES")
print("=" * 60)

# Étape 1 : Connexion
print("\n🔐 Étape 1 : Connexion...")
login_data = {
    "username": "test_vendeur2",
    "password": "Password123!"
}
login_response = requests.post(f"{BASE_URL}/auth/connexion/", json=login_data)

if login_response.status_code != 200:
    print("❌ Échec de connexion.")
    exit()

token = login_response.json().get('access')
headers = {"Authorization": f"Bearer {token}"}
print("✅ Connexion réussie !")

# Étape 2 : Créer un client
print("\n👤 Étape 2 : Créer un client...")
client_data = {
    "nom": "Jean Client",
    "telephone": "05050505",
    "email": "jean@client.com",
    "adresse": "Rue du Commerce, Abidjan"
}

response = requests.post(f"{BASE_URL}/commandes/clients/", json=client_data, headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 201:
    print("✅ Client créé !")
    client_id = response.json().get('id')
else:
    # Client existe déjà, on le récupère
    response = requests.get(f"{BASE_URL}/commandes/clients/", headers=headers)
    clients = response.json()
    if clients:
        client_id = clients[0]['id']
        print(f"ℹ️ Client existant utilisé (ID: {client_id})")
    else:
        print("❌ Aucun client disponible")
        exit()

# Étape 3 : Créer une commande
print("\n📝 Étape 3 : Créer une commande...")

# D'abord, récupérer un produit
response = requests.get(f"{BASE_URL}/produits/", headers=headers)
produits = response.json()

if not produits:
    print("❌ Aucun produit disponible. Créez d'abord des produits.")
    exit()

produit_id = produits[0]['id']

commande_data = {
    "client": client_id,
    "adresse_livraison": "Rue du Commerce, Abidjan",
    "ville": "Abidjan",
    "telephone_livraison": "05050505",
    "frais_livraison": "1000",
    "notes": "Livraison rapide svp",
    "lignes": [
        {
            "produit_id": produit_id,
            "quantite": 2
        }
    ]
}

response = requests.post(f"{BASE_URL}/commandes/", json=commande_data, headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 201:
    print("✅ Commande créée avec succès !")
    print(f"Référence: {response.json().get('reference')}")
    print(f"Total: {response.json().get('total_final')} FCFA")
    commande_id = response.json().get('id')
else:
    print(f"❌ Échec: {response.json()}")
    commande_id = 1

# Étape 4 : Lister les commandes
print("\n📋 Étape 4 : Lister mes commandes...")
response = requests.get(f"{BASE_URL}/commandes/", headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    commandes = response.json()
    print(f"✅ {len(commandes)} commande(s) trouvée(s)")
    for c in commandes[:3]:
        print(f"   - {c['reference']}: {c['total_final']} FCFA ({c['statut_display']})")

# Étape 5 : Statistiques
print("\n📊 Étape 5 : Statistiques des commandes...")
response = requests.get(f"{BASE_URL}/commandes/stats/", headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    stats = response.json()
    print("✅ Statistiques:")
    print(f"   Total commandes: {stats.get('total_commandes')}")
    print(f"   En attente: {stats.get('en_attente')}")
    print(f"   Validées: {stats.get('validees')}")
    print(f"   Livrées: {stats.get('livrees')}")
    print(f"   Chiffre d'affaires: {stats.get('chiffre_affaires')} FCFA")

# Étape 6 : Changer le statut d'une commande
print("\n🔄 Étape 6 : Changer le statut d'une commande...")
statut_data = {"statut": "validee"}
response = requests.patch(f"{BASE_URL}/commandes/{commande_id}/statut/", json=statut_data, headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    print(f"✅ Statut mis à jour: {response.json().get('statut_display')}")

print("\n" + "=" * 60)
print("✅ TESTS COMMANDES TERMINÉS !")
print("=" * 60)