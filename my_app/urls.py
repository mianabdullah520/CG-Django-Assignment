from django.urls import path
from .views import create_user, get_user, ingest_stock_data, get_stock_data, post_transaction, get_user_transactions, get_user_transactions_by_timestamp

urlpatterns = [
    path('users/', create_user, name='create_user'),
    path('users/<str:username>/', get_user, name='get_user'),
    path('stocks/', ingest_stock_data, name='ingest_stock_data'),
    path('stocks/<str:ticker>/', get_stock_data, name='get_stock_data'),
    path('transactions/', post_transaction, name='post_transaction'),
    path('transactions/<int:user_id>/', get_user_transactions, name='get_user_transactions'),
    path('transactions/<int:user_id>/<str:start_timestamp>/<str:end_timestamp>/', get_user_transactions_by_timestamp, name='get_user_transactions_by_timestamp'),
]
