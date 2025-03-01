from itertools import count
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10,choices=[('income','Income'), ('expense','Expense')])
    category = models.CharField(max_length=100)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.type} - {self.amount}"