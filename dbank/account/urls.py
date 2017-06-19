from django.conf.urls import url

from .views import ClientListView, ClientDetailView, AccountListView, \
    TransactionListView, AccountCreate, TransactionCreate, AccountCreateReadView

app_name = 'bank'


urlpatterns = [
    # url(r'^$', HomePage.as_view(), name='home'),
    url(r'clients/$', ClientListView.as_view(), name='clients_list'),
    url(r'clients/(?P<pk>\d+)$', ClientDetailView.as_view(), name='clients_detail'),

    # REST API
    url(r'api/accounts/$', AccountCreateReadView.as_view(), name='accounts_rest_api'),

    url(r'accounts/$', AccountListView.as_view(), name='accounts_list'),
    url(r'accounts/create$', AccountCreate.as_view(), name='accounts_create'),
    url(r'accounts/(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account_transactions'),
    url(r'transactions/$', TransactionListView.as_view(), name='transactions_list'),
    url(r'transactions/create$', TransactionCreate.as_view(), name='transactions_create'),



]
