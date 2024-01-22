from rest_framework import serializers
from .models import Users, StockData, Transactions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'username', 'balance']

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ['ticker', 'open_price', 'close_price', 'high', 'low', 'volume', 'timestamp']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['transaction_id', 'user_id', 'ticker', 'transaction_type', 'transaction_volume', 'transaction_price', 'timestamp']
        read_only_fields = ['transaction_price', 'timestamp']