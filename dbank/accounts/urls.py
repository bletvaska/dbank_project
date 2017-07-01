from django.conf.urls import url
from rest_framework import routers
from transactions.views import TransactionListView

from .views import AccountListView, AccountCreate, AccountViewSet


# app_name = 'accounts'

urlpatterns = [
    url(r'^accounts$', AccountListView.as_view(), name='accounts_list'),
    url(r'^accounts/create$', AccountCreate.as_view(), name='accounts_create'),
    url(r'^accounts/(?P<account_id>\d+)/transactions$', TransactionListView.as_view(), name='account_transactions'),
]

# rest api
router = routers.DefaultRouter()
router.register(r'api/v1/accounts', AccountViewSet, base_name='accounts')
urlpatterns += router.urls