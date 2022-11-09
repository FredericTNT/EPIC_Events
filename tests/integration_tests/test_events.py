import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import User


@pytest.mark.django_db
def test_api_experience():
    """
    API experience :
    - Connexion administrateur (x@y.com)
    - Création d'un nouveau client (DC@magic.com)
    - Liste des clients
    - Mise à jour du contact commercial (a@b.com) du client DC@magic.com
    - Connexion utilisateur de l'équipe support (c@d.com)
    - Refus mise à jour du client DC@magic.com
    - Connexion utilisateur de l'équipe commerciale (b@c.com)
    - Refus mise à jour du client DC@magic.com
    - Connexion utilisateur de l'équipe commerciale (a@b.com)
    - Mise à jour du client DC@magic.com
    """
    client = APIClient()

#   Vérification du chargement de la base de test
    utilisateur = User.objects.get(email="a@b.com")
    expected_response = "Guillaume_le_conquérant"
    assert utilisateur.username == expected_response
    print("Database... OK")

#   Connexion administrateur
    url = reverse('token_obtain_pair')
    response = client.post(url, {'email': "x@y.com", 'password': "azerty"}, format='json')
    assert response.status_code == 200
    print(url, "Test Token Obtain... OK")
    jwt = response.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)

#   Création d'un nouveau client
    data_client = {'first_name': "David", 'last_name': "Copperfield", 'email': "DC@magic.com",
                   'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "The Magic World"}

    url = reverse('client-list')
    response = client.post(url, data_client, format='json')
    expected_response = "DC@magic.com"
    assert response.status_code == 201
    assert response.data['email'] == expected_response
    id_new_client = response.data['id']
    print(url, "Create Client... OK")

#   Liste des clients
    url = reverse('client-list')
    response = client.get(url)
    expected_response = 3
    assert response.status_code == 200
    assert response.data['count'] == expected_response
    print(url, "Clients list... OK")

#   Refus mise à jour du contact commercial du client DC@magic.com
    data_client = {'first_name': "David", 'last_name': "Copperfield", 'email': "DC@magic.com", 'sales_contact': 3,
                   'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "The New Magic World"}

    url = reverse('client-detail', kwargs={'pk': id_new_client})
    response = client.put(url, data_client, format='json')
    assert response.status_code == 400
    data = response.data['sales_contact'][0].title()
    expected_response = "Le contact doit appartenir à l'équipe commerciale"
    assert data.find(expected_response)
    print(url, "Update Client sales_contact Fail... OK")

#   Mise à jour du contact commercial (a@b.com) du client DC@magic.com
    data_client = {'first_name': "David", 'last_name': "Copperfield", 'email': "DC@magic.com", 'sales_contact': 2,
                   'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "The Magic World"}

    url = reverse('client-detail', kwargs={'pk': id_new_client})
    response = client.put(url, data_client, format='json')
    expected_response = 2
    assert response.status_code == 200
    assert response.data['sales_contact'] == expected_response
    print(url, "Update Client... OK")

#   Connexion utilisateur de l'équipe support (c@d.com)
    url = reverse('token_obtain_pair')
    response = client.post(url, {'email': "c@d.com", 'password': "s3cr3T!78"}, format='json')
    assert response.status_code == 200
    print(url, "Test Token Obtain... OK")
    jwt = response.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)

#   Refus mise à jour du client DC@magic.com
    data_client = {'first_name': "David", 'last_name': "Copperfield", 'email': "DC@magic.com", 'sales_contact': 2,
                   'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "The New Magic World"}

    url = reverse('client-detail', kwargs={'pk': id_new_client})
    response = client.put(url, data_client, format='json')
    assert response.status_code == 403
    data = response.data['detail'][0].title()
    expected_response = "Vous n'avez pas la permission d'effectuer cette action"
    assert data.find(expected_response)
    print(url, "Update Client Fail... OK")

#   Connexion utilisateur de l'équipe commerciale (b@c.com)
    url = reverse('token_obtain_pair')
    response = client.post(url, {'email': "b@c.com", 'password': "s3cr3T!78"}, format='json')
    assert response.status_code == 200
    print(url, "Test Token Obtain... OK")
    jwt = response.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)

#   Refus mise à jour du client DC@magic.com
    data_client = {'first_name': "David", 'last_name': "Copperfield", 'email': "DC@magic.com", 'sales_contact': 2,
                   'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "The New Magic World"}

    url = reverse('client-detail', kwargs={'pk': id_new_client})
    response = client.put(url, data_client, format='json')
    assert response.status_code == 403
    data = response.data['detail'][0].title()
    expected_response = "Vous n'avez pas la permission d'effectuer cette action"
    assert data.find(expected_response)
    print(url, "Update Client Fail... OK")

#   Connexion utilisateur de l'équipe commerciale (a@b.com)
    url = reverse('token_obtain_pair')
    response = client.post(url, {'email': "a@b.com", 'password': "s3cr3T!78"}, format='json')
    assert response.status_code == 200
    print(url, "Test Token Obtain... OK")
    jwt = response.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)

#   Mise à jour du client DC@magic.com
    data_client = {'first_name': "David", 'last_name': "Copperfield", 'email': "DC@magic.com", 'sales_contact': 2,
                   'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "The New Magic World"}

    url = reverse('client-detail', kwargs={'pk': id_new_client})
    response = client.put(url, data_client, format='json')
    expected_response = "The New Magic World"
    assert response.status_code == 200
    assert response.data['company_name'] == expected_response
    print(url, "Update Client... OK")
