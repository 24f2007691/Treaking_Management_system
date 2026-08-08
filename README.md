# Trekking Management Application

A role-based web application built using Flask for managing trekking events. The application provides separate dashboards for Administrators, Trek Staff, and Users (trekkers), enabling trek creation, staff assignment, booking management, and participant tracking through a single platform.

---

## Project Overview

Managing trekking events manually becomes difficult as the number of treks, staff, and participants grows. This application digitizes the process with three distinct roles — Admin, Trek Staff, and User — each with its own dashboard and permissions, keeping trek management organized and centralized.

---

## Features

### Admin
- Create, edit, and delete treks
- Approve or blacklist trek staff registrations
- Assign staff members to treks
- View all users, staff, treks, and bookings
- Blacklist users
- Dashboard summary: total treks, users, staff, and bookings

### Trek Staff
- Register and log in (requires admin approval before access)
- View treks assigned to them
- Update available slots and trek status
- View participants booked on their assigned treks

### User (Trekker)
- Register and log in
- Browse currently open treks
- Book a trek (with slot availability and duplicate-booking checks)
- View and cancel their own bookings
- Update profile details

### System-level
- Role-based access control (admin / staff / user) enforced per route via session checks
- Prevention of overbooking (slot count decremented/incremented on booking/cancellation)
- Staff accounts gated behind admin approval before they can log in
- Blacklisted accounts blocked at login

---

## Technology Stack

**Backend:** Python, Flask
**Database / ORM:** SQLite, Flask-SQLAlchemy
**Frontend:** HTML5, CSS3, Jinja2 templates
**Session handling:** Flask's built-in session (`session["user_id"]`, `session["role"]`)

---

## Project Structure
