import requests

BASE_URL = "http://127.0.0.1:8000/api/auth"

print("=" * 50)
print("🔐 TEST AUTHENTIFICATION API")
print("=" * 50)

# Test 1 : Inscription
print("\n📝 Test 1 : Inscription...")
data_inscription = {
    "username": "vendeur1",
    "email": "vendeur1@saas.com",
    "first_name": "Jean",
    "last_name": "Test",
    "telephone": "07070707",
    "lien_site": "jean-boutique",
    "password": "Password123!",
    "password_confirmation": "Password123!"
}

try:
    response = requests.post(f"{BASE_URL}/inscription/", json=data_inscription)
    print(f"Statut: {response.status_code}")
    if response.status_code == 201:
        print("✅ Inscription réussie !")
        token = response.json().get('access')
        print(f"Token: {token[:50]}...")
    else:
        print(f"❌ Échec: {response.json()}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 2 : Connexion
print("\n🔑 Test 2 : Connexion...")
data_connexion = {
    "username": "vendeur1",
    "password": "Password123!"
}

try:
    response = requests.post(f"{BASE_URL}/connexion/", json=data_connexion)
    print(f"Statut: {response.status_code}")
    if response.status_code == 200:
        print("✅ Connexion réussie !")
        token = response.json().get('access')
        print(f"Token: {token[:50]}...")
    else:
        print(f"❌ Échec: {response.json()}")
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "=" * 50)
print("✅ Tests terminés !")
print("=" * 50)