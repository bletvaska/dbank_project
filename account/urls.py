from django.conf.urls import url

from account.views import ClientListView, ClientDetailView, AccountListView, AccountTransactionListView, \
    TransactionListView

app_name = 'bank'


urlpatterns = [
    # url(r'hello', Hello.as_view(), name='hello'),
    # url(r'^$', HomePage.as_view(), name='home'),
    url(r'clients/$', ClientListView.as_view(), name='clients_list'),
    url(r'clients/(?P<pk>\d+)$', ClientDetailView.as_view(), name='clients_detail'),
    url(r'accounts/$', AccountListView.as_view(), name='accounts_list'),
    url(r'accounts/(?P<account_id>\d+)/transactions$', AccountTransactionListView.as_view(), name='account_transactions'),
    url(r'transactions/$', TransactionListView.as_view(), name='transactions_list'),
]
