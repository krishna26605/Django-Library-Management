from django.urls import path
from django.contrib import admin
from .views import (
    home_view, admin_login_page, admin_signup_page, 
    AdminSignupView, AdminLoginView, 
    BookListCreateView, BookRetrieveUpdateDeleteView, StudentBookListView, 
    book_list_view, book_list_api
)

urlpatterns = [
    # ✅ Home Page
    path('', home_view, name='home'),

    # ✅ Django Admin Panel
    path('admin/', admin.site.urls),

    # ✅ Admin Authentication Routes
    path('admin-signup/', admin_signup_page, name='admin_signup_page'),
    path('api/admin/signup/', AdminSignupView.as_view(), name='admin_signup'),  
    path('api/admin/login/', AdminLoginView.as_view(), name='admin_login'),  
    path('admin-login/', admin_login_page, name='admin_login'),

    # ✅ Books Management
    path('books/', BookListCreateView.as_view(), name='book_list_create'),
    path('books/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book_detail'),
    path('book-list/', book_list_view, name='book_list_html'),
    path('api/books/', book_list_api, name='book_list_api'),

    # ✅ Student Books
    path('student/books/', StudentBookListView.as_view(), name='student_books'),
]


