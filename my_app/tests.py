from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from .models import Users, StockData, Transactions

class YourAppTests(TestCase):

    def test_create_user(self):
        url = reverse('create_user')
        data = {'username': 'test_user', 'balance': 1000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 1)
        self.assertEqual(Users.objects.get().username, 'test_user')

    def test_get_user(self):
        user = Users.objects.create(username='test_user', balance=1000)
        url = reverse('get_user', kwargs={'username': 'test_user'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test_user')

    def test_ingest_stock_data(self):
        url = reverse('ingest_stock_data')
        data = {'ticker': 'AAPL', 'open_price': 150, 'close_price': 155, 'high': 160, 'low': 145, 'volume': 100000, 'timestamp': '2022-01-25T12:00:00Z'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StockData.objects.count(), 1)
        self.assertEqual(StockData.objects.get().ticker, 'AAPL')

    def test_get_stock_data(self):
        stock = StockData.objects.create(ticker='AAPL', open_price=150, close_price=155, high=160, low=145, volume=100000, timestamp='2022-01-25T12:00:00Z')
        url = reverse('get_stock_data', kwargs={'ticker': 'AAPL'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ticker'], 'AAPL')

    def test_post_transaction(self):
        user = Users.objects.create(username='test_user', balance=1000)
        stock = StockData.objects.create(ticker='AAPL', open_price=150, close_price=155, high=160, low=145, volume=100000, timestamp='2022-01-25T12:00:00Z')
        url = reverse('post_transaction')
        data = {'user_id': user.id, 'ticker': 'AAPL', 'transaction_type': 'buy', 'transaction_volume': 10}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transactions.objects.count(), 1)
        self.assertEqual(Transactions.objects.get().user_id, user.id)

    def test_get_user_transactions(self):
        user = Users.objects.create(username='test_user', balance=1000)
        url = reverse('get_user_transactions', kwargs={'user_id': user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Assuming no transactions for the user initially

    def test_get_user_transactions_by_timestamp(self):
        user = Users.objects.create(username='test_user', balance=1000)
        url = reverse('get_user_transactions_by_timestamp', kwargs={'user_id': user.id, 'start_timestamp': '2022-01-25T00:00:00Z', 'end_timestamp': '2022-01-25T23:59:59Z'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Assuming no transactions for the user initially

