from django.conf.urls import url
from .views import TransactionListView, TransactionCreate

# app_name = 'transactions'

urlpatterns = [
    url(r'^$', TransactionListView.as_view(), name='transactions_list'),
    url(r'create$', TransactionCreate.as_view(), name='transactions_create'),
]
