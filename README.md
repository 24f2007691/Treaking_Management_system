# Trekking Management Application

A role-based web application built using Flask for managing trekking activities. The application provides separate dashboards for Administrators, Trek Staff, and Users (Trekkers), allowing trek management, staff assignment, booking management, and participant tracking through a single platform.

---

## Project Overview

Managing trekking activities manually can become difficult when the number of treks, staff members, and participants increases.

The Trekking Management Application provides a simple centralized system to manage these activities digitally.

The application has three main roles:

- Administrator
- Trek Staff
- User (Trekker)

Each role has its own dashboard and permissions.

The Administrator manages treks, users, staff, and bookings. Trek Staff members manage the treks assigned to them, while Users can browse available treks and make or cancel bookings.

---

## Features

### Admin

- Create new treks
- Edit existing treks
- Delete treks
- Approve trek staff registrations
- Blacklist trek staff
- Assign staff members to treks
- View all users
- View all trek staff
- View all treks
- View all bookings
- Blacklist users
- View dashboard statistics
- Manage trek information and staff assignments

### Trek Staff

- Register as trek staff
- Log in after administrator approval
- View assigned treks
- View trek details
- Update available trek slots
- Update trek status
- View participants registered for assigned treks

### User (Trekker)

- Register as a user
- Log in to the application
- Browse currently open treks
- View trek details
- Book a trek
- View their bookings
- Cancel their bookings
- Update profile information

### System Features

- Role-based access control
- Session-based authentication
- Admin approval for trek staff
- Prevention of duplicate bookings
- Prevention of booking when no slots are available
- Automatic slot reduction after booking
- Automatic slot restoration after cancellation
- Blacklisted accounts are prevented from logging in
- Staff can manage only their assigned treks

---

## Technology Stack

### Backend

- Python
- Flask

### Database

- SQLite
- Flask-SQLAlchemy

### Frontend

- HTML5
- CSS3
- Jinja2 Templates

### Authentication and Session Handling

- Flask built-in session

The application uses Flask sessions to store the logged-in user's ID and role.

---

## Project Structure

```text
Trekking_Management_Application/
│
├── app.py
├── models.py
├── Creating_admin.py
├── README.md
├── requirements.txt
│
├── instance/
│   └── trekking_app_database.sqlite3
│
└── templates/
    │
    ├── authentication/
    │   ├── index.html
    │   ├── register.html
    │   └── register_staff.html
    │
    ├── admin/
    │   ├── dashboard.html
    │   ├── treks.html
    │   ├── trek_form.html
    │   ├── assign_staff.html
    │   ├── staff.html
    │   ├── users.html
    │   └── bookings.html
    │
    ├── staff/
    │   ├── dashboard.html
    │   ├── trek_detail.html
    │   └── participants.html
    │
    └── user/
        ├── dashboard.html
        ├── treks.html
        ├── trek_detail.html
        ├── bookings.html
        └── profile.html
````

---

## Database Design

The application uses SQLite as its database and Flask-SQLAlchemy for database operations.

The database contains four main tables:

* users
* trek_staff
* treks
* bookings

---

### Users

The `users` table stores the details of application users.

| Field      | Type     | Notes                 |
| ---------- | -------- | --------------------- |
| id         | Integer  | Primary Key           |
| name       | String   | Not Null              |
| age        | Integer  | Not Null              |
| email      | String   | Unique, Not Null      |
| password   | String   | Not Null              |
| mobile     | String   | Not Null              |
| address    | String   | Not Null              |
| role       | String   | admin / staff / user  |
| status     | String   | Account status        |
| created_at | DateTime | Default: Current Time |

The `role` field determines the type of account:

* `admin`
* `staff`
* `user`

The `status` field is used for account management.

---

### Trek Staff

The `trek_staff` table stores additional information about trek staff members.

| Field             | Type    | Notes                          |
| ----------------- | ------- | ------------------------------ |
| id                | Integer | Primary Key                    |
| trek_staff_name   | String  | Not Null                       |
| phone             | String  | Not Null                       |
| experience        | Integer | Not Null                       |
| address           | String  | Not Null                       |
| emergency_contact | String  | Not Null                       |
| user_id           | Integer | Foreign Key → users.id, Unique |

The `user_id` connects a trek staff profile with its corresponding user account.

---

### Treks

The `treks` table stores information about trekking activities.

| Field             | Type    | Notes                                 |
| ----------------- | ------- | ------------------------------------- |
| id                | Integer | Primary Key                           |
| trek_name         | String  | Not Null                              |
| location          | String  | Not Null                              |
| difficulty        | String  | Not Null                              |
| duration          | Integer | Not Null                              |
| available_slots   | Integer | Not Null                              |
| start_date        | Date    | Trek start date                       |
| end_date          | Date    | Trek end date                         |
| status            | String  | Trek status                           |
| assigned_staff_id | Integer | Foreign Key → trek_staff.id, Nullable |

The `assigned_staff_id` field is nullable because a trek can exist without a staff member being assigned.

---

### Bookings

The `bookings` table stores information about trek bookings.

| Field          | Type     | Notes                  |
| -------------- | -------- | ---------------------- |
| id             | Integer  | Primary Key            |
| user_id        | Integer  | Foreign Key → users.id |
| trek_id        | Integer  | Foreign Key → treks.id |
| booking_date   | DateTime | Default: Current Time  |
| booking_status | String   | Booked / Cancelled     |
| payment_status | String   | Payment status         |

The `user_id` connects the booking to the trekker and the `trek_id` connects the booking to the selected trek.

---

## Database Relationships

The main relationships in the application are:

* A User can have multiple Bookings.
* A User can have one Trek Staff profile.
* A Trek Staff member can be assigned to multiple Treks.
* A Trek can have multiple Bookings.
* A Trek can have one assigned Trek Staff member.
* A Booking belongs to one User and one Trek.

---

## Application Flow

### Admin Flow

```text
Admin Login
     |
     v
Admin Dashboard
     |
     +---- Manage Users
     |
     +---- Manage Staff
     |
     +---- Manage Treks
     |
     +---- Assign Staff
     |
     +---- View Bookings
```

### Trek Staff Flow

```text
Staff Registration
       |
       v
Pending Approval
       |
       v
Admin Approval
       |
       v
Staff Login
       |
       v
Staff Dashboard
       |
       +---- View Assigned Treks
       |
       +---- Manage Trek
       |
       +---- View Participants
```

### User Flow

```text
User Registration
       |
       v
User Login
       |
       v
User Dashboard
       |
       +---- Browse Treks
       |
       +---- View Trek Details
       |
       +---- Book Trek
       |
       +---- View Bookings
       |
       +---- Cancel Booking
       |
       +---- Update Profile
```

---

## Authentication and Authorization

The application uses Flask's built-in session functionality for authentication.

After a successful login, the application stores information such as:

```python
session["user_id"]
session["role"]
```

The user's role is checked before accessing protected routes.

The three roles have different access levels:

| Role  | Access                                          |
| ----- | ----------------------------------------------- |
| Admin | Users, Staff, Treks, Bookings, Staff Assignment |
| Staff | Assigned Treks and Participants                 |
| User  | Available Treks and Own Bookings                |

This provides basic role-based access control without using additional authentication libraries.

---

## Staff Approval Process

Trek Staff members cannot directly access the staff dashboard after registration.

The process is:

```text
Staff Registration
       ↓
Pending
       ↓
Admin Reviews Staff
       ↓
Approved
       ↓
Staff Can Login
```

If a staff member is blacklisted, the account cannot be used to access the application.

---

## Trek Booking Process

The booking process works as follows:

1. The user logs in.
2. The user opens the available trek list.
3. The user selects a trek.
4. The user views the trek details.
5. The user selects the booking option.
6. The application checks whether the trek is open.
7. The application checks whether slots are available.
8. The application checks whether the user already has an active booking for the same trek.
9. If all conditions are satisfied, the booking is created.
10. The available slot count is reduced by one.

### Booking Cancellation

When a user cancels a booking:

1. The booking status is changed to `Cancelled`.
2. The available slot count is increased by one.

This helps prevent overbooking and keeps the available slot count updated.

---

## Business Rules

* Only approved staff members can log in as Trek Staff.
* Blacklisted accounts cannot log in.
* Staff members can only manage treks assigned to them.
* Users can only book treks whose status is `Open`.
* Users cannot book a trek when there are no available slots.
* A user cannot have multiple active bookings for the same trek.
* Available slots decrease when a booking is made.
* Available slots increase when a booking is cancelled.
* Only the Administrator can assign staff members to treks.
* Only the Administrator can approve or blacklist staff members.

---

## Installation

### 1. Clone the Repository

Replace the placeholder with your GitHub repository URL.

```bash
git clone <your-repository-url>
cd Trekking_Management_Application
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not being used, the required packages can also be installed directly:

```bash
pip install flask flask-sqlalchemy
```

### 5. Create the Admin Account

Run the admin creation script once:

```bash
python Creating_admin.py
```

This creates the database tables and creates the administrator account if an administrator does not already exist.

### 6. Run the Application

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

Open the address in a web browser.

---

## Admin Login

The administrator credentials are created through `Creating_admin.py`.

```text
Email: <add-your-admin-email>
Password: <add-your-admin-password>
```

Replace the above placeholders with your credentials if you want to include them in the final README.

---

## Requirements

The project requires:

```text
Flask
Flask-SQLAlchemy
```

A `requirements.txt` file can contain:

```text
Flask
Flask-SQLAlchemy
```

---

## Known Limitations

This project is designed as a basic educational application.

Some current limitations are:

* Passwords are currently stored as plain text.
* No email notification system is implemented.
* No online payment gateway is implemented.
* No advanced search and filtering system is implemented.
* The application uses basic HTML and CSS for the user interface.

---

## Future Improvements

The application can be extended in the future with:

* Password hashing using Werkzeug
* Search and filtering of treks
* Email notifications
* Online payment integration
* Trek images
* Ratings and reviews
* Improved form validation
* More detailed dashboard statistics
* Better error handling
* Improved user interface

---

## Author

**Name:** Sujal Pareek

**Roll Number:** 24f2007691


## License

This project was developed for educational purposes as part of an academic project.



