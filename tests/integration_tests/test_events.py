import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import User


@pytest.mark.django_db
def test_events():

    client = APIClient()

    utilisateurs = User.objects.count()
    expected_response = 4
    assert utilisateurs == expected_response

    data_user = {'email': "TNT@Cameroun.com", 'username': "Perroquette_du_Gabon",
                 'password1': "secret!78", 'password2': "secret!78",
                 'first_name': "Chloé", 'last_name': "CAMEROUN"}

    url = reverse('register')
    response = client.post(url, data_user, format='json')
    expected_response = "Perroquette_du_Gabon"
    assert response.status_code == 201
    assert response.data['username'] == expected_response
    print(url, "Test Create User... OK")

    url = reverse('token_obtain_pair')
    response = client.post(url, {'email': "a@b.com", 'password': "s3cr3T!78"}, format='json')
    assert response.status_code == 200
    print(url, "Test Token Obtain... OK")
    jwt = response.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)

#   Test Create Client
    data_client = {'first_name': "David", 'last_name': "Copperfield", 'email': "DC@magic.com",
                   'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "The Magic World"}

    url = reverse('client-list')
    response = client.post(url, data_client, format='json')
    expected_response = "DC@magic.com"
    assert response.status_code == 201
    assert response.data['email'] == expected_response
    print(url, "Test Create Client... OK")

    url = reverse('client-detail', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200
    print(url, "CLIENT", response.data)

#   Test Create Contract
    data_contract = {'amount': "3500.78", 'payment_due': "2023-07-22", 'status': False, 'client': 1}

    url = reverse('contract-list')
    response = client.post(url, data_contract, format='json')
    expected_response = "3500.78"
    assert response.status_code == 201
    assert response.data['amount'] == expected_response
    print(url, "Test Create Contract... OK")

    url = reverse('contract-detail', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200
    print(url, "CONTRAT", response.data)
