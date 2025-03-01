from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Transaction
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    # transactions=Transaction.objects.all()
    # income_sum = sum(t.amount for t in transactions if t.type== "income" )
    # expense_sum = sum(t.amount for t in transactions if t.type== "expense" )
    # balance = income_sum-expense_sum
    return render(request, "home.html")


@login_required(login_url='login')
def add_transaction(request):
    if request.method == "POST":
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['date']
        type = request.POST['type']
        
        
        Transaction.objects.create(user=request.user,amount=amount, type=type, category=category, date=date)
        return redirect('transaction')
    return render(request, "addtransaction.html")

@login_required(login_url='login')
def transaction(request):
    transactions=Transaction.objects.filter(user=request.user)
    income_sum = sum(t.amount for t in transactions if t.type== "income" )
    expense_sum = sum(t.amount for t in transactions if t.type== "expense" )
    balance = income_sum-expense_sum
    return render(request, "transactions.html", 
                  {'transactions' : transactions,
                   'income_sum' : income_sum,
                   'expense_sum' : expense_sum,
                   'balance' : balance
                   })

def delete_transaction(request,id):
    transactions = get_object_or_404(Transaction,id=id,user=request.user)
    transactions.delete()
    return redirect('transaction')
