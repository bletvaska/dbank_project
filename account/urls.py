from django.conf.urls import url
from django.urls import reverse

from account.views import ClientListView, ClientDetailView, AccountListView, AccountTransactionListView, \
    TransactionListView, AccountCreate, TransactionCreate

app_name = 'bank'


urlpatterns = [
    # url(r'hello', Hello.as_view(), name='hello'),
    # url(r'^$', HomePage.as_view(), name='home'),
    url(r'clients/$', ClientListView.as_view(), name='clients-list'),
    url(r'clients/(?P<pk>\d+)$', ClientDetailView.as_view(), name='clients-detail'),
    url(r'accounts/$', AccountListView.as_view(), name='accounts-list'),
    url(r'accounts/create$', AccountCreate.as_view(), name='accounts-create'),
    url(r'accounts/(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account-transactions'),
    url(r'transactions/$', TransactionListView.as_view(), name='transactions-list'),
    url(r'transactions/create$', TransactionCreate.as_view(), name='transactions-create'),
]
