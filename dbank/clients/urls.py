from django.conf.urls import url
from clients.views import DashboardView, ClientViewSet

# app_name = 'clients'
from rest_framework import routers

urlpatterns = [
    url(r'^clients/dashboard$', DashboardView.as_view(), name='dashboard')
]

# rest api
router = routers.DefaultRouter()
router.register(r'api/v1/clients', ClientViewSet, base_name='clients')
urlpatterns += router.urls
