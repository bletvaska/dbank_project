from django.conf.urls import url
from transactions.views import TransactionListView

from .views import AccountListView, AccountCreate


# router = routers.DefaultRouter()
# router.register(r'api/accounts', AccountViewSet, base_name='accounts')
# router.register(r'api/clients', ClientViewSet, base_name='client')
# router.register(r'api/transactions', TransactionViewSet, base_name='transaction')
# urlpatterns = router.urls

app_name = 'accounts'

urlpatterns = [
    # url(r'my/dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^$', AccountListView.as_view(), name='accounts_list'),
    url(r'^create$', AccountCreate.as_view(), name='accounts_create'),
    url(r'^(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account_transactions'),


]

