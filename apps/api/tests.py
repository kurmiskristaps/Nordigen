from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from django.test.utils import override_settings

from celery.exceptions import Retry

from django.db import connections

from celery import app  # your Celery app
import threading

# for python 2: use mock.patch from `pip install mock`.
from unittest.mock import patch

from .tasks import fetch_balances

class IndexViewTests(TestCase):
    def test_index_view_succeeds(self):
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class AuthViewTests(TestCase):
    def test_auth_view_succeeds(self):
        url = reverse('auth', args=['123'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class AuthViewTests(TestCase):
    def test_detail_view_without_requisitiom_redirects(self):
        s = self.client.session
        s.update({
            "req_id": '',
        })
        s.save()

        url = reverse('details')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/index')


    def test_detail_view_with_requisitiom_succeeds(self):
        s = self.client.session
        s.update({
            "req_id": '123',
        })
        s.save()

        url = reverse('details')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

class CeleryTestCase(TransactionTestCase):
    """Test case with Celery support."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app.control.purge()
        cls._worker = app.Worker(app=app, pool='solo', concurrency=1)
        connections.close_all()
        cls._thread = threading.Thread(target=cls._worker.start)
        cls._thread.daemon = True
        cls._thread.start()

    @classmethod
    def tearDownClass(cls):
        cls._worker.stop()
        super().tearDownClass()
    # @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    #     CELERY_ALWAYS_EAGER=True,
    #     BROKER_BACKEND='memory')
    def test_get_transactions_with_no_account_id_fails(self):
        s = self.client.session
        s.update({
            "token": {'access':'123'},
        })
        s.save()

        url = reverse('get-balances')
        with patch('apps.api.views.fetch_details.delay') as mock_task:

            response = self.client.get(url, {'account_id': '123'})
            task_id = response.data['task_id']
            result = mock_task.AsyncResult(task_id).get()

        # response = self.client.get(url, {'account_id': 'hch', 'date_from': '2022-01-01', 'date_to': '2022-02-01', 'country': 'LV'})

        print(response)
        print(response.context)
        self.assertEqual(response.status_code, 200)


