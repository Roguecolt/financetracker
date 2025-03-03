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
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request,"Email format invalid")
            return render(request, 'signup.html')


        if password!=password2:
            messages.error(request, "Passwords dont match")
            return render(request, "signup.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "signup.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "signup.html")
        
        user = User.objects.create_user(username=username,email=email,password=password)
        user.is_active = False
        user.save()
        
        messages.success(request, "Account created successfully! Please check your email to verify your account.")
        return redirect("login")
    
    return render(request, 'signup.html')
        

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
