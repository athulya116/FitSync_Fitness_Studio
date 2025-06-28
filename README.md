# FitSync - Fitness Studio Booking API

A Django-based web app and REST API for class booking and schedule management.

## 🚀 Features

* User registration & login
* Book fitness classes
* View upcoming/past bookings
* REST APIs for `/classes`, `/book-class`, `/bookings`

## 🔧 Setup Instructions

```bash
git clone https://github.com/yourname/fitsync.git
cd fitsync
python -m venv venv
source venv/Scripts/activate 
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata seed_data.json  # Load sample seed data
python manage.py runserver
```

## 👤 Test Credentials

### 🔓 User Logins

* **Email:** `athulya@gmail.com`

* **Password:** `123456`

* **Email:** `praveen@gmail.com`

* **Password:** `123456`

### 🔑 Admin Login

* **Username:** `admin`
* **Password:** `admin`

Access admin panel at: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## 📥 Sample API Requests

### ✅ GET All Upcoming Classes

**URL:** `http://127.0.0.1:8000/classes`
**Method:** `GET`
**Response:**

```json
[
  {
    "class_type": "zumba",
    "date": "2025-07-01",
    "start_time": "07:00 AM",
    "end_time": "08:00 AM",
    "available_seats": 5
  },
  ...
]
```

### ✅ GET Bookings by Email

**URL:** `http://127.0.0.1:8000/bookings/?email=praveen@gmail.com`
**Method:** `GET`
**Response:**

```json
{
  "upcoming": [...],
  "history": [...]
}
```

### ✅ POST Book a Class

**URL:** `http://127.0.0.1:8000/book-class/`
**Method:** `POST`
**Headers:** `Content-Type: application/json`
**Body:**

```json
{
  "email": "athulya@gmail.com",
  "slot_id": 4
}
```

**Response:**

```json
{
  "message": "Class booked successfully!"
}
```

## 📁 Contents

* `seed_data.json`: Seed data for testing
* `README.md`: Setup and documentation

##


 
