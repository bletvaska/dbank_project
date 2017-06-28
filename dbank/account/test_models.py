import pytest
from django.db import IntegrityError

from .models import Account


@pytest.mark.django_db
def test_when_no_owner_is_provided_then_raise_IntegrityError():
    account = Account(iban='jano')
    with pytest.raises(IntegrityError):
        account.save()

# @pytest.mark.django_db
# def test_when_wrong_iban_is_given_then_raise_exception_X():
#     account = Account(iban='jano', owner='jano')
#     account.save()