from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Users, StockData, Transactions
from .serializers import UserSerializer, StockDataSerializer, TransactionSerializer
from django.utils import timezone
from django.db.models import Sum

@api_view(['POST', 'GET'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_user(request, username):
    if request.method == 'GET':
        user = get_object_or_404(Users, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['POST', 'GET'])
def ingest_stock_data(request):
    if request.method == 'POST':
        serializer = StockDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        stock_data = StockData.objects.all()
        serializer = StockDataSerializer(stock_data, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_stock_data(request, ticker):
    if request.method == 'GET':
        stock_data = get_object_or_404(StockData, ticker=ticker)
        serializer = StockDataSerializer(stock_data)
        return Response(serializer.data)


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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_transactions(request, user_id):
    if request.method == 'GET':
        transactions = Transactions.objects.filter(user_id=user_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_user_transactions_by_timestamp(request, user_id, start_timestamp, end_timestamp):
    if request.method == 'GET':
        transactions = Transactions.objects.filter(user_id=user_id, timestamp__range=[start_timestamp, end_timestamp])
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
