from django.conf.urls import url
from .views import TransactionListView, TransactionCreate

# app_name = 'transactions'

urlpatterns = [
    url(r'^transactions/$', TransactionListView.as_view(), name='transactions_list'),
    url(r'transactions/create$', TransactionCreate.as_view(), name='transactions_create'),
]
