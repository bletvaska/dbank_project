from django.conf.urls import url

from .views import ClientListView, ClientDetailView, AccountListView, \
    TransactionListView, AccountCreate, TransactionCreate

from .views import AccountListAPIView

app_name = 'bank'


urlpatterns = [
    # url(r'^$', HomePage.as_view(), name='home'),
    url(r'api/accounts/$', AccountListAPIView.as_view(), name='account_list_api'),
    url(r'clients/$', ClientListView.as_view(), name='clients-list'),
    url(r'clients/(?P<pk>\d+)$', ClientDetailView.as_view(), name='clients-detail'),
    url(r'accounts/$', AccountListView.as_view(), name='accounts-list'),
    url(r'accounts/create$', AccountCreate.as_view(), name='accounts-create'),
    url(r'accounts/(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account-transactions'),
    url(r'transactions/$', TransactionListView.as_view(), name='transactions-list'),
    url(r'transactions/create$', TransactionCreate.as_view(), name='transactions-create'),

]
