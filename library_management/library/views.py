from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Book
from django.contrib import messages
from django.contrib.auth.models import User



def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return render(request, 'library/signup.html')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'library/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'library/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, 'library/signup.html')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        login(request, user)
        return redirect('home')

    return render(request, 'library/signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'library/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'library/home.html')

def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})
