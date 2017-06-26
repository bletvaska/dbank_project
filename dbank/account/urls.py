from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from .views import AccountListView, \
    TransactionListView, AccountCreate, TransactionCreate, DashboardView, \
    AccountViewSet, ClientViewSet, TransactionViewSet


router = routers.DefaultRouter()
router.register(r'api/accounts', AccountViewSet, base_name='account')
router.register(r'api/clients', ClientViewSet, base_name='client')
router.register(r'api/transactions', TransactionViewSet, base_name='transaction')
urlpatterns = router.urls

schema_view = get_swagger_view(title='dBank API')

# app_name = 'bank'

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'my/dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'my/accounts/$', AccountListView.as_view(), name='accounts_list'),
    url(r'my/accounts/create$', AccountCreate.as_view(), name='accounts_create'),
    url(r'my/accounts/(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account_transactions'),
    url(r'my/transactions/$', TransactionListView.as_view(), name='transactions_list'),
    url(r'my/transactions/create$', TransactionCreate.as_view(), name='transactions_create'),
    url(r'^docs/$', schema_view),
]

