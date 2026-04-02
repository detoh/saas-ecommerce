from django.urls import path
from .views import DashboardVendeurView, DashboardAdminView

urlpatterns = [
    path('vendeur/', DashboardVendeurView.as_view(), name='dashboard-vendeur'),
    path('admin/', DashboardAdminView.as_view(), name='dashboard-admin'),
]