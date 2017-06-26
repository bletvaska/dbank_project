from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import ClientListView, ClientDetailView, AccountListView, \
    TransactionListView, AccountCreate, TransactionCreate, TransactionViewSet, AccountViewSet

app_name = 'bank'

transaction_router = DefaultRouter()
transaction_router.register(r'api/transactions', TransactionViewSet)

account_router = DefaultRouter()
account_router.register(r'api/accounts', AccountViewSet)

urlpatterns = transaction_router.urls + account_router.urls

urlpatterns += [
    # url(r'^$', HomePage.as_view(), name='home'),
    # url(r'api/accounts/$', AccountListAPIView.as_view(), name='account_list_api'),
    # url(r'api/transactions/$', TransactionListAPIView.as_view(), name='transaction_list_api'),

    url(r'clients/$', ClientListView.as_view(), name='clients_list'),
    url(r'clients/(?P<pk>\d+)$', ClientDetailView.as_view(), name='clients_detail'),
    url(r'accounts/$', AccountListView.as_view(), name='accounts_list'),
    url(r'accounts/create$', AccountCreate.as_view(), name='accounts_create'),
    url(r'accounts/(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account_transactions'),
    url(r'transactions/$', TransactionListView.as_view(), name='transactions_list'),
    url(r'transactions/create$', TransactionCreate.as_view(), name='transactions_create'),

]
