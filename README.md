# 📚 Django Library Management System - Documentation

## 📝 Project Overview
Django Library Management System is a web-based application that helps in managing books, users, and authentication in a library. It provides CRUD operations for books and allows admin authentication using JWT authentication.

## 🚀 Features
- Admin signup & login (JWT-based authentication)
- Full CRUD functionality for books (Add, View, Edit, Delete)
- Separate views for Admin and Students
- RESTful API endpoints
- Django authentication & session management

## 🛠️ Technologies Used
- **Backend:** Django, Django REST Framework (DRF)
- **Frontend:** HTML, CSS, JavaScript (if applicable)
- **Database:** MySQL
- **Authentication:** JWT (Simple JWT)

---

# ⚙️ Installation & Setup

## 1️⃣ Prerequisites
Ensure you have the following installed:
- Python 3.10+
- MySQL Server
- Virtual Environment (`venv`)
- Django & Dependencies

## 2️⃣ Clone the Repository
```sh
git clone https://github.com/krishna26605/Django-Library-Management.git
cd Django-Library-Management
```

## 3️⃣ Set Up Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## 4️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

## 5️⃣ Configure Database (MySQL)
Edit `settings.py` with your MySQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 6️⃣ Run Migrations
```sh
python manage.py makemigrations
python manage.py migrate
```

## 7️⃣ Create Superuser (Admin)
```sh
python manage.py createsuperuser
```
Provide details when prompted.

## 8️⃣ Run Development Server
```sh
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in the browser.

---

# 📌 API Endpoints

## 🔐 Authentication APIs
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/admin/signup/` | POST | Register an admin user |
| `/api/admin/login/` | POST | Login admin (returns JWT token) |

## 📚 Books APIs
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/books/` | GET | List all books |
| `/api/books/` | POST | Add a new book |
| `/api/books/{id}/` | GET | Retrieve a book by ID |
| `/api/books/{id}/` | PUT | Update a book |
| `/api/books/{id}/` | DELETE | Delete a book |

## 🎓 Student View APIs
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/student/books/` | GET | View books available for students |

---

# 🛠️ Troubleshooting
**1️⃣ MySQL connection error?**
- Check `settings.py` for correct database credentials.
- Ensure MySQL server is running.

**2️⃣ Login redirecting back to login page?**
- Check session settings in `settings.py`:
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
```

**3️⃣ Static files not loading?**
```sh
python manage.py collectstatic
```

---

# 🤝 Contributing
1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Open a pull request.

---

# 📞 Support
For issues, contact: [krishnaanikam26@gmail.com](mailto:krishnaanikam26@gmail.com) or open an issue in the repository.

Happy coding! 🎉

