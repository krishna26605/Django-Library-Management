from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .models import Book
from .serializers import AdminSerializer, BookSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# ✅ API to list books (JSON response)
@api_view(['GET'])
@permission_classes([AllowAny])
def book_list_api(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# ✅ Book List View (For UI)
def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})


# ✅ Home Page View
@login_required
def home_view(request):
    print("✅ DEBUG: home_view() function executed")  # ✅ Check if this line prints
    print(f"✅ DEBUG: User in Home View = {request.user}")  # ✅ Check if user is logged in

    return render(request, 'library/home.html', {"user": request.user})  # ✅ Ensure this is rendering HTML


# ✅ Student Books View
def student_books_view(request):
    return render(request, 'library/student_books.html')


# ✅ Admin Login & Signup Pages
def admin_login_page(request):
    return render(request, 'library/admin_login.html')

def admin_signup_page(request):
    return render(request, 'library/admin_signup.html')


# ✅ Admin Signup API (Now Redirects on Success or Failure)
class AdminSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if User.objects.filter(email=email).exists():
            return redirect('admin_login')  # ✅ Redirect to login if email exists

        user = User.objects.create_user(email=email, password=password)
        return redirect('admin_login')  # ✅ Redirect to login after successful signup


# ✅ Admin Login API (Now Redirects to Home)
@method_decorator(csrf_exempt, name='dispatch')
class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        print(f"🔍 DEBUG: Email = {email}, Password = {'*' * len(password) if password else 'None'}")  # Debug input

        if not email or not password:
            print("❌ DEBUG: Email or password missing")
            return Response({"error": "Email and password required"}, status=400)


        user = authenticate(username=email, password=password)
        print(f"🔍 DEBUG: Authenticated User = {user}")  # Debug authentication

        if user is None:
            print("❌ DEBUG: Invalid credentials")
            return Response({"error": "Invalid credentials"}, status=401)

        login(request, user)
        print(f"✅ DEBUG: User logged in, Session Key = {request.session.session_key}")

        # ✅ Ensure session is saved
        request.session['user_id'] = user.id
        request.session.modified = True

        response = Response({"message": "Login successful", "redirect_url": "/home/"}, status=200)
        response.set_cookie("sessionid", request.session.session_key)  # ✅ Set session cookie
        return response  # ✅ Return proper response


# ✅ CRUD for Books (Admin Only)
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ✅ Student View (View All Books)
class StudentBookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Students don't need authentication
