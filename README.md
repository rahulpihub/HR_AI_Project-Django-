
# SNS HR GEN AI TOOLS

This is a Django-based web application designed for [SNS HR GEN AI TOOLS ]. The project leverages Django's Model-View-Template (MVT) architecture to deliver a scalable and robust web application.

---

## Features
- **Dynamic Routing**: Fully functional URL routing system.
- **Responsive Design**: Integrated CSS and JavaScript for a seamless user experience.
- **Database Integration**: SQLite3 database for quick setup and local development.
- **Extensible Templates**: Modular and reusable templates for dynamic content rendering.

---

## Project Structure
```
new_django/
├── manage.py                  # Django's management script
├── README.md                  # Project documentation
├── db.sqlite3                 # SQLite database file
├── requirements.txt           # Python dependencies
├── generators/                # Django app with core functionality
│   ├── migrations/            # Database migrations
│   ├── templates/generators/  # HTML templates for the app
│   ├── static/css             # Static assets (CSS, JS, Images)
│   ├── admin.py               # Django admin site configuration
│   ├── models.py              # Database models
│   ├── views.py               # Request handling logic
│   └── urls.py                # App-specific URL routing
└── myproject/                 # Django project configuration
    ├── settings.py            # Project settings
    ├── urls.py                # Project-wide URL routing
    ├── wsgi.py                # WSGI entry point
    └── asgi.py                # ASGI entry point
```

---

## Prerequisites
- Python 3.x
- Django 4.x
- SQLite3

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd new_django
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000`.

---

## Usage
1. **Navigate to the Application**: Open your browser and visit `http://127.0.0.1:8000`.
2. **Admin Panel**: Use Django's admin panel at `/admin` (ensure you've created a superuser).
3. **Templates**: Customize the HTML templates in `generators/templates/` as needed.
4. **Static Files**: Add or update CSS, JavaScript, or images in `generators/static/`.

---

## Customization
- **Database**: Replace SQLite with a production-ready database (e.g., PostgreSQL).
- **Templates**: Modify `base.html` for global styling and layout.
- **Static Files**: Add custom styles and scripts in the `static/` directory.

---


