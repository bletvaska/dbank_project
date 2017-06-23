from django.conf.urls import url, include
from rest_framework import routers

from .views import AccountListView, \
    TransactionListView, AccountCreate, TransactionCreate, DashboardView, \
    AccountViewSet, ClientViewSet, TransactionViewSet

# app_name = 'bank'

router = routers.DefaultRouter()
router.register(r'api/accounts', AccountViewSet, base_name='account')
router.register(r'api/clients', ClientViewSet, base_name='client')
router.register(r'api/transactions', TransactionViewSet, base_name='transaction')
urlpatterns = router.urls

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'api/accounts/$', AccountCreateReadView.as_view(), name='account_list_api'),
    # url(r'api/transactions/$', TransactionCreateReadView.as_view(), name='transaction_list_api'),

    url(r'dashboard/$', DashboardView.as_view(), name='dashboard'),

    url(r'accounts/$', AccountListView.as_view(), name='accounts_list'),
    url(r'accounts/create$', AccountCreate.as_view(), name='accounts_create'),
    url(r'accounts/(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account_transactions'),
    url(r'transactions/$', TransactionListView.as_view(), name='transactions_list'),
    url(r'transactions/create$', TransactionCreate.as_view(), name='transactions_create'),
]

