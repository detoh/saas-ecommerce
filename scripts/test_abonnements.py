import requests

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("📊 TEST SYSTÈME D'ABONNEMENTS SaaS")
print("=" * 60)

# Étape 1 : Connexion
print("\n🔐 Étape 1 : Connexion...")
login_data = {
    "username": "admin_test",
    "password": "Password123!"
}
login_response = requests.post(f"{BASE_URL}/auth/connexion/", json=login_data)

if login_response.status_code != 200:
    print("❌ Échec de connexion.")
    exit()

token = login_response.json().get('access')
headers = {"Authorization": f"Bearer {token}"}
print("✅ Connexion réussie !")

# Étape 2 : Vérifier l'abonnement actuel
print("\n📋 Étape 2 : Vérifier mon abonnement...")
response = requests.get(f"{BASE_URL}/abonnements/actif/", headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    print("✅ Abonnement actif trouvé !")
    abo = response.json()
    print(f"   Plan: {abo.get('plan_display')}")
    print(f"   Statut: {abo.get('statut_display')}")
    print(f"   Jours restants: {abo.get('jours_restants')}")
else:
    print("ℹ️ Aucun abonnement actif")

# Étape 3 : Créer un abonnement
print("\n📝 Étape 3 : Créer un abonnement...")
abo_data = {
    "plan": "basic",
    "type_abo": "mensuel",
    "paiement_auto": False
}

response = requests.post(f"{BASE_URL}/abonnements/creer/", json=abo_data, headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 201:
    print("✅ Abonnement créé !")
    data = response.json()
    print(f"   Plan: {data['abonnement'].get('plan_display')}")
    print(f"   Prix: {data['abonnement'].get('prix')} FCFA")
    print(f"   Message: {data.get('message')}")
    print(f"   Montant à payer: {data.get('montant_a_payer')} FCFA")
else:
    print(f"Réponse: {response.json()}")

# Étape 4 : Statistiques
print("\n📈 Étape 4 : Statistiques d'abonnement...")
response = requests.get(f"{BASE_URL}/abonnements/stats/", headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    stats = response.json()
    print("✅ Statistiques:")
    print(f"   Total abonnements: {stats.get('total_abonnements')}")
    print(f"   Jours restants: {stats.get('jours_restants')}")
    print(f"   Expirable bientôt: {stats.get('expirable_bientot')}")

# Étape 5 : Vérification
print("\n✅ Étape 5 : Vérification d'abonnement...")
response = requests.get(f"{BASE_URL}/abonnements/verification/", headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"   Actif: {data.get('actif')}")
    print(f"   Plan: {data.get('plan')}")
    print(f"   Jours restants: {data.get('jours_restants')}")

print("\n" + "=" * 60)
print("✅ TESTS ABONNEMENTS TERMINÉS !")
print("=" * 60)