import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import User


@pytest.mark.django_db
class TestEvents:

    client = APIClient()

    def test_user_count(self):
        utilisateurs = User.objects.count()
        expected_response = 4
        assert utilisateurs == expected_response

    def test_register_ok(self):
        data_user = {'email': "TNT@Cameroun.com", 'username': "Perroquette_du_Gabon",
                     'password1': "secret!78", 'password2': "secret!78",
                     'first_name': "Chloé", 'last_name': "CAMEROUN"}

        url = reverse('register')
        response = self.client.post(url, data_user, format='json')
        expected_response = "Perroquette_du_Gabon"
        assert response.status_code == 201
        assert response.data['username'] == expected_response

    def test_register_fail_email(self):
        data_user = {'email': "a@b.com", 'username': "Perroquette_du_Gabon",
                     'password1': "secret!78", 'password2': "secret!78",
                     'first_name': "Chloé", 'last_name': "CAMEROUN"}

        url = reverse('register')
        response = self.client.post(url, data_user, format='json')
        assert response.status_code == 400
        data = response.data['email'][0].title()
        expected_response = "Un objet Utilisateur avec ce champ email existe déjà"
        assert data.find(expected_response)

    def test_register_fail_password(self):
        data_user = {'email': "TNT@Cameroun.com", 'username': "Perroquette_du_Gabon",
                     'password1': "secret!78", 'password2': "secret!79",
                     'first_name': "Chloé", 'last_name': "CAMEROUN"}

        url = reverse('register')
        response = self.client.post(url, data_user, format='json')
        assert response.status_code == 400
        data = response.data['password'][0].title()
        expected_response = "Les deux mots de passe ne sont pas identiques"
        assert data.find(expected_response)

    def test_token_ok(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': "a@b.com", 'password': "s3cr3T!78"}, format='json')
        assert response.status_code == 200
        jwt = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt)

    def test_token_fail_email(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': "fail@email.com", 'password': "s3cr3T!78"}, format='json')
        assert response.status_code == 401
        data = response.data['detail'][0].title()
        expected_response = "Aucun compte actif n'a été trouvé avec les identifiants fournis"
        assert data.find(expected_response)

    def test_token_fail_password(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': "a@b.com", 'password': "s3cr3T!79"}, format='json')
        assert response.status_code == 401
        data = response.data['detail'][0].title()
        expected_response = "Aucun compte actif n'a été trouvé avec les identifiants fournis"
        assert data.find(expected_response)

    def test_create_client_ok(self, mocker):
        data_client = {'first_name': "Marie-Antoinette", 'last_name': "Queen", 'email': "MAQ@princess.com",
                       'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "La Royauté"}

        mocker.patch('rest_framework.permissions.DjangoModelPermissions.has_permission', return_value=True)
        mocker.patch('events.permissions.IsChangeClientAuthorized.has_permission', return_value=True)

        url = reverse('client-list')
        response = self.client.post(url, data_client, format='json')
        expected_response = "MAQ@princess.com"
        assert response.status_code == 201
        assert response.data['email'] == expected_response

    def test_create_client_fail_permission(self, mocker):
        data_client = {'first_name': "Marie-Antoinette", 'last_name': "Queen", 'email': "MAQ@princess.com",
                       'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "La Royauté"}

        mocker.patch('rest_framework.permissions.DjangoModelPermissions.has_permission', return_value=False)
        mocker.patch('events.permissions.IsChangeClientAuthorized.has_permission', return_value=True)

        url = reverse('client-list')
        response = self.client.post(url, data_client, format='json')
        assert response.status_code == 403
        data = response.data['detail'][0].title()
        expected_response = "Vous n'avez pas la permission d'effectuer cette action"
        assert data.find(expected_response)

    def test_create_client_fail_team(self, mocker):
        data_client = {'first_name': "Marie-Antoinette", 'last_name': "Queen", 'email': "MAQ@princess.com",
                       'phone': "+33112345678", 'mobile': "+33612345678", 'company_name': "La Royauté"}

        mocker.patch('rest_framework.permissions.DjangoModelPermissions.has_permission', return_value=True)
        mocker.patch('events.permissions.IsChangeClientAuthorized.has_permission', return_value=False)

        url = reverse('client-list')
        response = self.client.post(url, data_client, format='json')
        assert response.status_code == 403
        data = response.data['detail'][0].title()
        expected_response = "Vous n'avez pas la permission d'effectuer cette action"
        assert data.find(expected_response)

    def test_create_contract_ok(self, mocker):
        data_contract = {'amount': "3500.78", 'payment_due': "2023-07-22", 'status': False, 'client': 2}

        mocker.patch('rest_framework.permissions.DjangoModelPermissions.has_permission', return_value=True)
        mocker.patch('events.permissions.IsChangeContractAuthorized.has_permission', return_value=True)

        url = reverse('contract-list')
        response = self.client.post(url, data_contract, format='json')
        expected_response = "3500.78"
        assert response.status_code == 201
        assert response.data['amount'] == expected_response

    def test_create_contract_fail_team(self, mocker):
        data_contract = {'amount': "3500.78", 'payment_due': "2023-07-22", 'status': False, 'client': 2}

        mocker.patch('rest_framework.permissions.DjangoModelPermissions.has_permission', return_value=True)
        mocker.patch('events.permissions.IsChangeContractAuthorized.has_permission', return_value=False)

        url = reverse('contract-list')
        response = self.client.post(url, data_contract, format='json')
        assert response.status_code == 403
        data = response.data['detail'][0].title()
        expected_response = "Vous n'avez pas la permission d'effectuer cette action"
        assert data.find(expected_response)

    def test_create_event_ok(self, mocker):
        data_event = {'date_event': "2023-07-22T22:00", 'guests': 61, 'notes': "Anniversaire surprise !...",
                      'status': 2, 'support_contact': 3, 'contract': 3}

        mocker.patch('rest_framework.permissions.DjangoModelPermissions.has_permission', return_value=True)
        mocker.patch('events.permissions.IsChangeEventAuthorized.has_permission', return_value=True)

        url = reverse('event-list')
        response = self.client.post(url, data_event, format='json')
        expected_response = 61
        assert response.status_code == 201
        assert response.data['guests'] == expected_response

    def test_create_event_fail_team(self, mocker):
        data_event = {'date_event': "2023-07-22T22:00", 'guests': 61, 'notes': "Anniversaire surprise !...",
                      'status': 2, 'support_contact': 3, 'contract': 3}

        mocker.patch('rest_framework.permissions.DjangoModelPermissions.has_permission', return_value=True)
        mocker.patch('events.permissions.IsChangeEventAuthorized.has_permission', return_value=False)

        url = reverse('event-list')
        response = self.client.post(url, data_event, format='json')
        assert response.status_code == 403
        data = response.data['detail'][0].title()
        expected_response = "Vous n'avez pas la permission d'effectuer cette action"
        assert data.find(expected_response)

    def test_create_event_fail_authorization(self, mocker):
        data_event = {'date_event': "2023-07-22T22:00", 'guests': 61, 'notes': "Anniversaire surprise !...",
                      'status': 2, 'support_contact': 3, 'contract': 3}

        mocker.patch('rest_framework.permissions.DjangoModelPermissions.has_permission', return_value=True)
        mocker.patch('events.permissions.IsChangeEventAuthorized.has_permission', return_value=True)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ')

        url = reverse('event-list')
        response = self.client.post(url, data_event, format='json')
        assert response.status_code == 401
        data = response.data['code'][0].title()
        expected_response = "bad_authorization_header"
        assert data.find(expected_response)
