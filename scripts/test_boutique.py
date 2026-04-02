import requests

BASE_URL = "http://127.0.0.1:8000/api"

# D'abord, connectez-vous pour obtenir un token
print("🔐 Connexion...")
login_data = {
    "username": "vendeur1",
    "password": "Password123!"
}
login_response = requests.post(f"{BASE_URL}/auth/connexion/", json=login_data)

if login_response.status_code != 200:
    print("❌ Échec de connexion. Créez d'abord un utilisateur.")
    exit()

token = login_response.json().get('access')
headers = {"Authorization": f"Bearer {token}"}

print("✅ Connexion réussie !")
print("=" * 50)

# Test 1 : Vérifier si on a déjà une boutique
print("\n🏪 Test 1 : Vérifier ma boutique...")
response = requests.get(f"{BASE_URL}/boutiques/ma-boutique/", headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 404:
    print("ℹ️ Aucune boutique trouvée, création en cours...")
    
    # Test 2 : Créer une boutique
    print("\n📝 Test 2 : Créer une boutique...")
    boutique_data = {
        "nom_boutique": "Ma Super Boutique",
        "theme": "moderne",
        "couleur_primaire": "#FF5733",
        "couleur_secondaire": "#FFFFFF",
        "devise": "XOF",
        "whatsapp_numero": "07070707"
    }
    
    response = requests.post(f"{BASE_URL}/boutiques/ma-boutique/", json=boutique_data, headers=headers)
    print(f"Statut: {response.status_code}")
    if response.status_code == 201:
        print("✅ Boutique créée avec succès !")
        print(f"Réponse: {response.json()}")
    else:
        print(f"❌ Échec: {response.json()}")
elif response.status_code == 200:
    print("✅ Vous avez déjà une boutique !")
    print(f"Réponse: {response.json()}")

# Test 3 : Lister les boutiques
print("\n📋 Test 3 : Lister mes boutiques...")
response = requests.get(f"{BASE_URL}/boutiques/", headers=headers)
print(f"Statut: {response.status_code}")
print(f"Réponse: {response.json()}")

print("\n" + "=" * 50)
print("✅ Tests boutiques terminés !")
print("=" * 50)