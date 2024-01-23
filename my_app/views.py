from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Users, StockData, Transactions
from .serializers import UserSerializer, StockDataSerializer, TransactionSerializer
from django.utils import timezone
from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


@api_view(['POST', 'GET'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # No need for caching in this view as it retrieves all users
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_user(request, username):
    # Implementation for GET /users/{username}/
    cache_key = f"user_{username}"
    user_data = cache.get(cache_key)

    if not user_data:
        user = get_object_or_404(Users, username=username)
        serializer = UserSerializer(user)
        user_data = serializer.data


        cache.set(cache_key, user_data, 300)

    return Response(user_data)

@api_view(['POST', 'GET'])
def ingest_stock_data(request):
    if request.method == 'POST':
        serializer = StockDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        cache_key = "all_stock_data"
        stock_data = cache.get(cache_key)

        if not stock_data:
            stock_data = StockData.objects.all()
            serializer = StockDataSerializer(stock_data, many=True)
            stock_data = serializer.data

    
            cache.set(cache_key, stock_data, 300)

        return Response(stock_data)

@api_view(['GET'])
def get_stock_data(request, ticker):
    cache_key = f"stock_data_{ticker}"
    stock_data = cache.get(cache_key)

    if not stock_data:
        stock_data = get_object_or_404(StockData, ticker=ticker)
        serializer = StockDataSerializer(stock_data)
        stock_data = serializer.data

    
        cache.set(cache_key, stock_data, 300)

    return Response(stock_data)

@api_view(['POST'])
def post_transaction(request):
    if request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(Users, user_id=request.data['user_id'])
            stock = get_object_or_404(StockData, ticker=request.data['ticker'])
            
            # Calculate transaction_price based on the current stock price
            transaction_price = stock.close_price * request.data['transaction_volume']
            
            # Update the user's balance
            if request.data['transaction_type'] == 'buy':
                user.balance -= transaction_price
            elif request.data['transaction_type'] == 'sell':
                user.balance += transaction_price
            user.save()

            serializer.save(transaction_price=transaction_price, timestamp=timezone.now())

            # Clear relevant caches after a new transaction
            cache.delete(f"user_transactions_{request.data['user_id']}")
            cache.delete(f"user_transactions_{request.data['user_id']}_{request.data['timestamp']}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_transactions(request, user_id):
    cache_key = f"user_transactions_{user_id}"
    transactions = cache.get(cache_key)

    if not transactions:
        transactions = Transactions.objects.filter(user_id=user_id)
        serializer = TransactionSerializer(transactions, many=True)
        transactions = serializer.data

    
        cache.set(cache_key, transactions, 300)

    return Response(transactions)

@api_view(['GET'])
def get_user_transactions_by_timestamp(request, user_id, start_timestamp, end_timestamp):
    cache_key = f"user_transactions_{user_id}_{start_timestamp}_{end_timestamp}"
    transactions = cache.get(cache_key)

    if not transactions:
        transactions = Transactions.objects.filter(user_id=user_id, timestamp__range=[start_timestamp, end_timestamp])
        serializer = TransactionSerializer(transactions, many=True)
        transactions = serializer.data

        
        cache.set(cache_key, transactions, 300)

    return Response(transactions)
