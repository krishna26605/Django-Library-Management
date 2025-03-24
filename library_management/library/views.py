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
from rest_framework.permissions import BasePermission

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
@login_required(login_url='/login/')
def book_list_view(request):
    print(f"✅ DEBUG: User in book_list_view = {request.user}")  
    print(f"✅ DEBUG: User is authenticated? {request.user.is_authenticated}")  # **Check if user is logged in**

    if not request.user.is_authenticated:
        return HttpResponse("❌ DEBUG: User is NOT authenticated!", status=403)

    return render(request, 'library/book_list.html', {'books': Book.objects.all()})

# ✅ Home Page View
@login_required(login_url='/admin-login/')
def home_view(request):
    return render(request, 'library/home.html', {"user": request.user})

# ✅ Admin Login View with Email Authentication
def admin_login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        # ✅ Purani session clear karein
        request.session.flush()

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id  # ✅ Store user ID in session
            request.session.modified = True  # ✅ Ensure session is saved

            print(f"✅ DEBUG: Login Successful! Session Key = {request.session.session_key}")
            return redirect('/')  # Redirect to home after login
        else:
            print("❌ DEBUG: Invalid credentials")
            return render(request, "library/admin_login.html", {"error": "Invalid credentials"})

    return render(request, "library/admin_login.html")


# ✅ Student Books View
def student_books_view(request):
    return render(request, 'library/student_books.html')

# ✅ Admin Login & Signup Pages
def admin_login_page(request):
    return render(request, 'library/admin_login.html')

def admin_signup_page(request):
    return render(request, 'library/admin_signup.html')

# ✅ Admin Signup API
class AdminSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if User.objects.filter(email=email).exists():
            return redirect('admin_login')

        user = User.objects.create_user(email=email, username=email, password=password)
        return redirect('admin_login')

# ✅ CRUD for Books (Admin Only)
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff  # ✅ Only admins

class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]  # ✅ Now only admins can delete books

# ✅ Student View (View All Books)
class StudentBookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
