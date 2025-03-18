from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect logged-in users to dashboard
    return redirect('login')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard instead of home
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST.get('email', '').strip()  # Get email and remove spaces
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif email and User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()  # Ensure the user is saved
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after signup

    return render(request, 'accounts/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')



def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/dashboard.html', {'user': request.user})
    else:
        return redirect('login') 