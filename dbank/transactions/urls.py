from django.conf.urls import url
from rest_framework import routers

from .views import TransactionListView, TransactionCreate, TransactionViewSet

# app_name = 'transactions'

urlpatterns = [
    url(r'^transactions/$', TransactionListView.as_view(), name='transactions_list'),
    url(r'transactions/create$', TransactionCreate.as_view(), name='transactions_create'),
]

# rest api
router = routers.DefaultRouter()
router.register(r'api/v1/transactions', TransactionViewSet, base_name='transactions')
urlpatterns += router.urls
