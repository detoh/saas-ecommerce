from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.paiements import webhooks
from apps.core.views import accueil

urlpatterns = [
    path('', accueil, name='accueil'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    
    # Webhooks Mobile Money
    path('webhooks/orange/', webhooks.webhook_orange, name='webhook-orange'),
    path('webhooks/wave/', webhooks.webhook_wave, name='webhook-wave'),
    path('webhooks/mtn/', webhooks.webhook_mtn, name='webhook-mtn'),
    path('webhooks/moov/', webhooks.webhook_moov, name='webhook-moov'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)