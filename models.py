from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class User(db.Model):
    __tablename__="users"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    mobile=db.Column(db.String(15),nullable=False)
    address=db.Column(db.String(255),nullable=False)
    role=db.Column(db.String(20),nullable=False)
    status=db.Column(db.String(20),default="Pending")
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    bookings=db.relationship("Booking",backref="user")
    staff_profile=db.relationship("TrekStaff",backref="user",uselist=False)


class TrekStaff(db.Model):
    __tablename__="trek_staff"

    id=db.Column(db.Integer,primary_key=True)
    trek_staff_name=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(15),nullable=False)
    experience=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(255),nullable=False)
    emergency_contact=db.Column(db.String(100),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),unique=True,nullable=False)

    assigned_treks=db.relationship("Trek",backref="staff")


class Trek(db.Model):
    __tablename__="treks"

    id=db.Column(db.Integer,primary_key=True)
    trek_name=db.Column(db.String(150),nullable=False)
    location=db.Column(db.String(100),nullable=False)
    difficulty=db.Column(db.String(20),nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    available_slots=db.Column(db.Integer,nullable=False)
    start_date=db.Column(db.Date)
    end_date=db.Column(db.Date)
    status=db.Column(db.String(20),default="Pending")
    assigned_staff_id=db.Column(db.Integer,db.ForeignKey("trek_staff.id"),nullable=False)

    bookings=db.relationship("Booking",backref="trek")


class Booking(db.Model):
    __tablename__="bookings"

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey("treks.id"),nullable=False)
    booking_date=db.Column(db.DateTime,default=datetime.utcnow)
    booking_status=db.Column(db.String(20),default="Booked")
    payment_status=db.Column(db.String(20),default="Pending")