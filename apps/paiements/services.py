import requests
from django.conf import settings
from .models import Paiement

class MobileMoneyService:
    """Service unifié pour les paiements Mobile Money"""
    
    @staticmethod
    def initier_paiement_orange(paiement, telephone, montant):
        """Initie un paiement Orange Money"""
        # Simulation d'appel API (à remplacer par la vraie API Orange)
        # Documentation: https://developer.orange.com/apis/payments
        
        url = "https://api.orange.com/orange-money-webpay/dev/v1/webpayment"
        
        headers = {
            'Authorization': f"Bearer {settings.MOBILE_MONEY_CONFIG.get('ORANGE', {}).get('API_KEY', '')}",
            'Content-Type': 'application/json',
        }
        
        data = {
            'merchant_key': settings.MOBILE_MONEY_CONFIG.get('ORANGE', {}).get('MERCHANT_KEY', ''),
            'order_id': paiement.reference_interne,
            'amount': str(montant),
            'currency': 'XOF',
            'customer_phone': telephone,
            'return_url': 'https://votresite.com/paiement/success',
            'cancel_url': 'https://votresite.com/paiement/cancel',
            'notif_url': 'https://votresite.com/webhooks/orange/',
        }
        
        try:
            # Pour le développement, on simule une réussite
            # response = requests.post(url, json=data, headers=headers)
            
            # SIMULATION POUR DÉVELOPPEMENT
            paiement.initier_paiement()
            paiement.operateur_response = {
                'status': 'initiated',
                'message': 'Paiement Orange Money initié. Veuillez valider sur votre téléphone.'
            }
            paiement.save()
            
            return {
                'success': True,
                'message': 'Paiement initié. Veuillez valider sur votre téléphone.',
                'data': paiement.operateur_response
            }
            
        except Exception as e:
            paiement.echouer_paiement(str(e))
            return {
                'success': False,
                'message': f'Erreur Orange Money: {str(e)}'
            }
    
    @staticmethod
    def initier_paiement_wave(paiement, telephone, montant):
        """Initie un paiement Wave"""
        # Documentation: https://developer.wave.com/
        
        url = "https://api.wave.com/v1/charge"
        
        headers = {
            'Authorization': f"Bearer {settings.MOBILE_MONEY_CONFIG.get('WAVE', {}).get('API_KEY', '')}",
            'Content-Type': 'application/json',
        }
        
        data = {
            'amount': int(montant),
            'currency': 'XOF',
            'phone': telephone,
            'reference': paiement.reference_interne,
            'webhook': 'https://votresite.com/webhooks/wave/',
        }
        
        try:
            # SIMULATION POUR DÉVELOPPEMENT
            paiement.initier_paiement()
            paiement.operateur_response = {
                'status': 'initiated',
                'message': 'Paiement Wave initié. Veuillez valider sur votre téléphone.'
            }
            paiement.save()
            
            return {
                'success': True,
                'message': 'Paiement initié. Veuillez valider sur votre téléphone.',
                'data': paiement.operateur_response
            }
            
        except Exception as e:
            paiement.echouer_paiement(str(e))
            return {
                'success': False,
                'message': f'Erreur Wave: {str(e)}'
            }
    
    @staticmethod
    def initier_paiement_mtn(paiement, telephone, montant):
        """Initie un paiement MTN Money"""
        # Documentation: https://momodeveloper.mtn.com/
        
        url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
        
        headers = {
            'X-Reference-Id': paiement.reference_interne,
            'X-Target-Environment': 'sandbox',
            'Authorization': f"Bearer {settings.MOBILE_MONEY_CONFIG.get('MTN', {}).get('API_KEY', '')}",
            'Content-Type': 'application/json',
        }
        
        data = {
            'amount': str(montant),
            'currency': 'XOF',
            'externalId': paiement.reference_interne,
            'payer': {
                'partyIdType': 'MSISDN',
                'partyId': telephone
            },
            'payerMessage': 'Paiement commande',
            'payeeNote': 'Merci pour votre achat'
        }
        
        try:
            # SIMULATION POUR DÉVELOPPEMENT
            paiement.initier_paiement()
            paiement.operateur_response = {
                'status': 'initiated',
                'message': 'Paiement MTN Money initié. Veuillez valider sur votre téléphone.'
            }
            paiement.save()
            
            return {
                'success': True,
                'message': 'Paiement initié. Veuillez valider sur votre téléphone.',
                'data': paiement.operateur_response
            }
            
        except Exception as e:
            paiement.echouer_paiement(str(e))
            return {
                'success': False,
                'message': f'Erreur MTN Money: {str(e)}'
            }
    
    @staticmethod
    def initier_paiement_moov(paiement, telephone, montant):
        """Initie un paiement Moov Money"""
        # Documentation: https://moov-africa.com/
        
        try:
            # SIMULATION POUR DÉVELOPPEMENT
            paiement.initier_paiement()
            paiement.operateur_response = {
                'status': 'initiated',
                'message': 'Paiement Moov Money initié. Veuillez valider sur votre téléphone.'
            }
            paiement.save()
            
            return {
                'success': True,
                'message': 'Paiement initié. Veuillez valider sur votre téléphone.',
                'data': paiement.operateur_response
            }
            
        except Exception as e:
            paiement.echouer_paiement(str(e))
            return {
                'success': False,
                'message': f'Erreur Moov Money: {str(e)}'
            }
    
    @classmethod
    def initier_paiement(cls, paiement, telephone, montant):
        """Méthode principale pour initier un paiement selon l'opérateur"""
        methode = paiement.methode
        
        if methode == 'orange_money':
            return cls.initier_paiement_orange(paiement, telephone, montant)
        elif methode == 'wave':
            return cls.initier_paiement_wave(paiement, telephone, montant)
        elif methode == 'mtn_money':
            return cls.initier_paiement_mtn(paiement, telephone, montant)
        elif methode == 'moov_money':
            return cls.initier_paiement_moov(paiement, telephone, montant)
        else:
            return {
                'success': False,
                'message': 'Méthode de paiement non supportée'
            }