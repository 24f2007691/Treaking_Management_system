# 🏔️ Trekking Management Application

A role-based web application built using **Flask** that simplifies the management of trekking events. The application allows administrators, trek staff, and trekkers to efficiently manage treks, bookings, staff assignments, and participant information through a centralized platform.

This project was developed as part of the **Application Development I** course in the **IIT Madras BS Degree in Data Science and Applications**.

---

# Project Overview

Managing trekking events manually can become challenging as the number of participants and staff grows. This application digitizes the entire process by providing separate dashboards for **Admin**, **Trek Staff**, and **Users**, making trek management organized, secure, and efficient.

The application supports trek creation, booking management, staff approval, participant tracking, and role-based access control.

---

# Features

## Admin

- Secure administrator login
- Create, edit, and delete treks
- Approve or reject trek staff registrations
- Assign staff members to treks
- View all users, staff, bookings, and treks
- Search users, staff, or treks using IDs or names
- Blacklist or deactivate users and staff
- Dashboard displaying:
  - Total Treks
  - Total Users
  - Total Staff
  - Total Bookings

---

## Trek Staff

- Register and log in
- Access dashboard after admin approval
- View assigned treks
- Update trek information
- Manage available slots
- Change trek status
- View registered participants

---

## Trekker (User)

- Register and log in
- Browse available treks
- Search treks by location and difficulty
- Book treks
- View booking history
- Track booking status
- Update profile details

---

## System Features

- Role-based authentication
- Authorization for each user role
- Prevention of overbooking
- Trek status management
- Booking history tracking
- Responsive Bootstrap interface
- SQLite database integration

---

# Technology Stack

## Backend

- Python
- Flask

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- Jinja2

## Database

- SQLite

## Python Libraries

- Flask-SQLAlchemy
- Flask-Login
- Werkzeug

---

# Project Structure

```text
Trekking-Management-Application/
│
├── app.py
├── models.py
├── config.py
├── requirements.txt
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/
│   ├── admin/
│   ├── staff/
│   ├── user/
│   └── base.html
│
├── instance/
│   └── trekking.db
│
└── README.md
```

---

# Database Design

## User

- User ID
- Name
- Email
- Password
- Role
- Status

## Staff

- Staff ID
- Name
- Contact Information
- Approval Status
- Assigned Treks

## Trek

- Trek ID
- Trek Name
- Location
- Difficulty
- Duration
- Available Slots
- Assigned Staff
- Start Date
- End Date
- Status

## Booking

- Booking ID
- User ID
- Trek ID
- Booking Date
- Booking Status

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/24f2007691/Trekking-Management-Application.git
cd Trekking-Management-Application
```

## Create a Virtual Environment

```bash
python -m venv venv
```

## Activate the Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

# Default Admin Account

```
Username : admin

Password : admin123
```

> The administrator account is created automatically during database initialization.

---

# Business Rules

- Only approved staff members can access the Staff Dashboard.
- Staff members can manage only their assigned treks.
- Users can book only treks that are currently open.
- Bookings are restricted when no slots are available.
- The administrator has full control over users, staff, bookings, and treks.
- Booking records are maintained for future reference.

---

# Future Improvements

- Email notifications
- Online payment gateway
- Trek image gallery
- Ratings and reviews
- Analytics dashboard
- PDF and Excel report generation
- REST API support
- Weather API integration

---

# Learning Outcomes

This project helped strengthen my understanding of:

- Flask Web Development
- SQLAlchemy ORM
- SQLite Database Design
- Authentication & Authorization
- CRUD Operations
- Role-Based Access Control
- Bootstrap Responsive Design
- MVC Architecture

---

# Author

**Sujal Pareek**

**Roll Number:** 24F2007691

**IIT Madras BS Degree in Data Science and Applications**

**GitHub:** https://github.com/24f2007691

---

# License

This project is developed solely for educational purposes as part of the **Application Development I** course in the **IIT Madras BS Degree in Data Science and Applications**.
