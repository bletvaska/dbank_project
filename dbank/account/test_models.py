import random
# import faker

import pytest
from django.db import IntegrityError

from .models import Account, Client

# @pytest.fixture(scope='module')
# def create_random_clients():
#     client = Client.

# @pytest.fixture()
# def random_client():
#     print(Account.objects.all())
#     return random.choice(Client.objects.all())
#
#
# @pytest.fixture()
# def random_account():
#     print(Account.objects.all())
#     return random.choice(Account.objects.all())


@pytest.mark.django_db
def test_when_no_owner_is_provided_then_raise_IntegrityError():
    account = Account(iban='jano')
    with pytest.raises(IntegrityError):
        account.save()


@pytest.mark.django_db
def test_when_account_with_same_iban_is_inserted_then_raise_IntegrityError():
    random_account = random.choice(Account.objects.all())
    random_client = random.choice(Client.objects.all())
    account = Account(iban=random_account.iban, owner=random_client)
    with pytest.raises(IntegrityError):
        account.save()


# @pytest.mark.django_db
# def test_when_wrong_iban_is_given_then_raise_exception_X():
#     account = Account(iban='jano', owner='jano')
#     account.save()
