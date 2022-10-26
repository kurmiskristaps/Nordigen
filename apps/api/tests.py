import datetime
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from unittest.mock import patch
from .forms import GetAccountIdForm, GetTransactionsForm
from nordigen import NordigenClient
from apps.api.views import NordigenClient
from nordigen.types import RequisitionDto

class IndexViewTests(TestCase):
    def test_without_errors_succeeds(self):
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    @patch('apps.api.views.NordigenClient.generate_token', **{'return_value.raiseError.side_effect': Exception()})
    def test_with_exception_renders_error(self, mock_generate_token):
        url = reverse('index')
        mock_generate_token.return_value = ''
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error.html')



class AuthViewTests(TestCase, NordigenClient):
    @patch('apps.api.views.NordigenClient.initialize_session')
    def test_with_valid_data_succeeds(self, mock_initialize_session):
        url = reverse('auth', args=['abc123'])
        data = RequisitionDto(
            link='http://localhost:8000/index/details', requisition_id='123'        
        )

        mock_initialize_session.return_value = data
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)


    def test_with_invalid_data_renders_error(self):
        url = reverse('auth', args=[{'abc': 123}])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error.html')


class DetailViewTests(TestCase):
    def test_without_requisitiom_redirects(self):
        s = self.client.session
        s.update({
            "req_id": '',
        })
        s.save()

        url = reverse('details')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/index')


    def test_with_requisitiom_succeeds(self):
        s = self.client.session
        s.update({
            "req_id": '123',
        })
        s.save()

        url = reverse('details')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class GetTransactionsTests(SimpleTestCase):
    def test_with_get_request_fails(self):
        url = reverse('get-transactions')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)


    def test_with_get_request_fails(self):
        url = reverse('get-transactions')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)


class GetBalancesTests(SimpleTestCase):
    def test_with_get_request_fails(self):
        url = reverse('get-balances')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)


    def test_with_get_request_fails(self):
        url = reverse('get-balances')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)


class GetDetailsTests(SimpleTestCase):
    def test_with_get_request_fails(self):
        url = reverse('get-details')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)


    def test_with_get_request_fails(self):
        url = reverse('get-details')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)


class GetAccountIdFormTests(SimpleTestCase):
    def test_with_no_id_fails(self):
        form_data = {'account_id': ''}
        form = GetAccountIdForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_with_valid_data_succeeds(self):
        form_data = {'account_id': '123abc'}
        form = GetAccountIdForm(data=form_data)
        self.assertTrue(form.is_valid())


class GetTransactionsFormTests(SimpleTestCase):
    def test_with_invalid_data_fails(self):
        tomorrow = str(datetime.date.today() + datetime.timedelta(1))
        form_data = (
            {'account_id': '', 'date_from': '2022-01-01', 'date_to': '2022-01-01', 'country': 'LV'},
            {'account_id': '123abc', 'date_from': '2022-01-02', 'date_to': '2022-01-01'},
            {'account_id': '123abc', 'date_from': tomorrow},
            {'account_id': '123abc', 'date_to': tomorrow},
            {'account_id': '123abc', 'country': 'LVA'},
            {'account_id': '123abc', 'country': 'L'},
        )

        for data in form_data:
            form = GetTransactionsForm(data=data)
            self.assertFalse(form.is_valid())
    

    def test_with_valid_data_succeeds(self):
        form_data = (
            {'account_id': '123abc', 'date_from': '', 'date_to': '', 'country': ''},
            {'account_id': '123abc', 'date_from': '2022-01-01', 'date_to': '2022-01-01', 'country': 'LV'},
            {'account_id': '123abc', 'date_from': '2022-01-01'},
            {'account_id': '123abc', 'date_to': '2022-01-01'},
        )

        for data in form_data:
            form = GetTransactionsForm(data=data)
            self.assertTrue(form.is_valid())
