from django.conf.urls import url

from .views import ClientDetailView, AccountListView, \
    TransactionListView, AccountCreate, TransactionCreate, APIAccountList, DashboardView

app_name = 'bank'


urlpatterns = [
    url(r'api/accounts/$', APIAccountList.as_view(), name='account_list_api'),

    # url(r'clients/(?P<pk>\d+)$', ClientDetailView.as_view(), name='clients_detail'),
    url(r'clients/$', ClientDetailView.as_view(), name='clients_detail'),
    url(r'dashboard/$', DashboardView.as_view(), name='dashboard'),

    url(r'accounts/$', AccountListView.as_view(), name='accounts_list'),
    url(r'accounts/create$', AccountCreate.as_view(), name='accounts_create'),
    url(r'accounts/(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account_transactions'),
    url(r'transactions/$', TransactionListView.as_view(), name='transactions_list'),
    url(r'transactions/create$', TransactionCreate.as_view(), name='transactions_create'),



]
