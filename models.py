from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Creating 'USER' TABLE


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)
    # admin
    # staff
    # trekker

    status = db.Column(db.String(20), default="pending")
    # pending
    # active
    # blacklisted

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships

    bookings = db.relationship(
        "Booking",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    assigned_treks = db.relationship(
        "Trek",
        back_populates="staff"
    )

    staff_profile = db.relationship(
        "StaffProfile",
        uselist=False,
        back_populates="user"
    )


# ------------------------
# TREK TABLE
# ------------------------

class Trek(db.Model):

    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    trek_name = db.Column(db.String(150), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    difficulty = db.Column(db.String(20), nullable=False)

    duration = db.Column(db.Integer, nullable=False)

    available_slots = db.Column(db.Integer, nullable=False)

    start_date = db.Column(db.Date)

    end_date = db.Column(db.Date)

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    assigned_staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    # Relationships

    staff = db.relationship(
        "User",
        back_populates="assigned_treks"
    )

    bookings = db.relationship(
        "Booking",
        back_populates="trek",
        cascade="all, delete-orphan"
    )


# ------------------------
# BOOKING TABLE
# ------------------------

class Booking(db.Model):

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    booking_status = db.Column(
        db.String(20),
        default="Booked"
    )

    payment_status = db.Column(
        db.String(20),
        default="Pending"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    # Relationships

    user = db.relationship(
        "User",
        back_populates="bookings"
    )

    trek = db.relationship(
        "Trek",
        back_populates="bookings"
    )


# ------------------------
# STAFF PROFILE TABLE
# ------------------------

class Trek_staff(db.Model):

    __tablename__ = "Trek_staff"

    id = db.Column(db.Integer, primary_key=True)

    phone = db.Column(db.String(20))

    experience = db.Column(db.Integer)

    emergency_contact = db.Column(db.String(100))

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True
    )

    user = db.relationship(
        "User",
        back_populates="Trek_staff"
    )