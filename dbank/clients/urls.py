from django.conf.urls import url
from clients.views import DashboardView

# app_name = 'clients'

urlpatterns = [
    url(r'^dashboard$', DashboardView.as_view(), name='dashboard')
]
