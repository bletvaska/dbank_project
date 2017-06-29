# import pytest
# import requests
#
# URL = "http://127.0.0.1:8000/bank/api/"
# HEADERS = {
#     'authorization': "Basic YmF0bWFuOmtvbnZhbGlua2ExMjM=",
#     'content-type': "application/json"
# }


# @pytest.fixture(scope='module')
# def session():
#     session = requests.Session()
#     yield session
#     session.close()


# def test_when_get_accounts_then_return_200(client):
#     response = client.get('/bank/api/accounts/')
#     assert response.status_code == 200


def test_when_no_authorization_is_provided_then_return_403(client):
    response = client.get('/bank/api/accounts/')
    assert response.status_code == 403
#
# def test_when_new_client_created_then_return_201(session):
#     pass
