from django.urls import path
from .views import home, add_transaction, transaction,delete_transaction

urlpatterns = [
    path('', view=home,name='home'),
    path('add/', view=add_transaction, name='add_transaction'),
    path('transactions/', view=transaction, name='transaction'),
    path('delete/<int:id>/', view=delete_transaction, name='delete_transaction'),
]