from django.conf.urls import url

from .views import AccountListView, AccountCreate


# router = routers.DefaultRouter()
# router.register(r'api/accounts', AccountViewSet, base_name='accounts')
# router.register(r'api/clients', ClientViewSet, base_name='client')
# router.register(r'api/transactions', TransactionViewSet, base_name='transaction')
# urlpatterns = router.urls
#
# schema_view = get_swagger_view(title='dBank API')

app_name = 'accounts'

urlpatterns = [
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'my/dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^$', AccountListView.as_view(), name='accounts_list'),
    url(r'^create$', AccountCreate.as_view(), name='accounts_create'),
    # url(r'^(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account_transactions'),
    # url(r'my/transactions/$', TransactionListView.as_view(), name='transactions_list'),
    # url(r'my/transactions/create$', TransactionCreate.as_view(), name='transactions_create'),
    # url(r'^docs/$', schema_view),
]

