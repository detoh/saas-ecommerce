from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Paiement
import json
import hashlib
import hmac

@csrf_exempt
def webhook_orange(request):
    """Webhook pour Orange Money"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        reference = data.get('order_id')
        statut = data.get('status')
        transaction_id = data.get('transaction_id')
        
        paiement = Paiement.objects.get(reference_interne=reference)
        
        if statut == 'SUCCESS':
            paiement.confirmer_paiement(transaction_id)
            return JsonResponse({'status': 'ok'})
        else:
            paiement.echouer_paiement(statut)
            return JsonResponse({'status': 'failed'})
            
    except Paiement.DoesNotExist:
        return JsonResponse({'error': 'Paiement non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def webhook_wave(request):
    """Webhook pour Wave"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        reference = data.get('reference')
        statut = data.get('status')
        transaction_id = data.get('id')
        
        paiement = Paiement.objects.get(reference_interne=reference)
        
        if statut == 'success':
            paiement.confirmer_paiement(transaction_id)
            return JsonResponse({'status': 'ok'})
        else:
            paiement.echouer_paiement(statut)
            return JsonResponse({'status': 'failed'})
            
    except Paiement.DoesNotExist:
        return JsonResponse({'error': 'Paiement non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def webhook_mtn(request):
    """Webhook pour MTN Money"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        reference = data.get('externalId')
        statut = data.get('status')
        transaction_id = data.get('transactionId')
        
        paiement = Paiement.objects.get(reference_interne=reference)
        
        if statut == 'SUCCESSFUL':
            paiement.confirmer_paiement(transaction_id)
            return JsonResponse({'status': 'ok'})
        else:
            paiement.echouer_paiement(statut)
            return JsonResponse({'status': 'failed'})
            
    except Paiement.DoesNotExist:
        return JsonResponse({'error': 'Paiement non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def webhook_moov(request):
    """Webhook pour Moov Money"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        reference = data.get('reference')
        statut = data.get('status')
        
        paiement = Paiement.objects.get(reference_interne=reference)
        
        if statut == 'success':
            paiement.confirmer_paiement()
            return JsonResponse({'status': 'ok'})
        else:
            paiement.echouer_paiement(statut)
            return JsonResponse({'status': 'failed'})
            
    except Paiement.DoesNotExist:
        return JsonResponse({'error': 'Paiement non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)