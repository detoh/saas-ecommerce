import requests

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("💰 TEST SYSTÈME DE PAIEMENT MOBILE MONEY")
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

# Étape 2 : Récupérer une commande
print("\n📋 Étape 2 : Récupérer une commande...")
response = requests.get(f"{BASE_URL}/commandes/", headers=headers)

if response.status_code != 200 or len(response.json()) == 0:
    print("❌ Aucune commande disponible. Créez d'abord une commande.")
    exit()

commande = response.json()[0]
commande_id = commande['id']
print(f"✅ Commande trouvée: {commande.get('reference')}")
print(f"   Total: {commande.get('total_final')} FCFA")

# Étape 3 : Initier un paiement Orange Money
print("\n📱 Étape 3 : Initier paiement Orange Money...")
paiement_data = {
    "commande_id": commande_id,
    "methode": "orange_money",
    "telephone": "07070707"
}

response = requests.post(f"{BASE_URL}/paiements/initier/", json=paiement_data, headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    print("✅ Paiement initié avec succès !")
    paiement = response.json().get('paiement')
    print(f"   Référence: {paiement.get('reference_interne')}")
    print(f"   Statut: {paiement.get('statut_display')}")
    print(f"   Montant: {paiement.get('montant')} FCFA")
    print(f"   Message: {response.json().get('message')}")
    paiement_id = paiement.get('id')
else:
    print(f"❌ Échec: {response.json()}")
    paiement_id = 1

# Étape 4 : Vérifier le statut du paiement
print("\n🔍 Étape 4 : Vérifier le statut du paiement...")
response = requests.get(f"{BASE_URL}/paiements/{paiement_id}/statut/", headers=headers)
print(f"Statut: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print("✅ Statut du paiement:")
    print(f"   Référence: {data.get('reference')}")
    print(f"   Statut: {data.get('statut_display')}")
    print(f"   Montant: {data.get('montant')} FCFA")
    print(f"   Méthode: {data.get('methode')}")

# Étape 5 : Simuler un webhook (pour test)
print("\n🔄 Étape 5 : Simuler confirmation webhook...")
print("   (Dans la production, c'est l'opérateur qui appelle ce webhook)")
print("   URL webhook Orange: http://127.0.0.1:8000/webhooks/orange/")

print("\n" + "=" * 60)
print("✅ TESTS PAIEMENT TERMINÉS !")
print("=" * 60)
print("\n📝 NOTES IMPORTANTES:")
print("   1. En production, les webhooks sont appelés par les opérateurs")
print("   2. Les URLs webhook doivent être accessibles publiquement")
print("   3. Configurez vos clés API dans settings.py")
print("   4. Testez en sandbox avant la production")
print("=" * 60)