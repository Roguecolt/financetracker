# Create your views here.
# users/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from tracker.models import Transaction  # Import transaction model
from django.contrib import messages
from django.contrib.auth.models import User
import json

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to user dashboard
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Convert email to username for authentication
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect after login
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard_view(request):
    # Fetch transactions for the logged-in user
    transactions = Transaction.objects.filter(user=request.user)
    
    income_sum = sum(t.amount for t in transactions if t.type == 'income')
    expense_sum = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income_sum - expense_sum
    
    chart_data = {
        'labels' : ['Income','Expense'],
        'values' : [float(income_sum) , float(expense_sum)]
    }

    return render(request, 'dashboard.html', {
        'total_income': income_sum,
        'total_expense': expense_sum,
        'balance': balance,
        'chart_data': json.dumps(chart_data),
    })
