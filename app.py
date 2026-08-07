from flask import Flask, render_template, request, session, redirect, url_for, flash
from models import *
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking_app_database.sqlite3"
app.secret_key = "secretkey"
db.init_app(app)


@app.route("/")
def home():
    return render_template("authentication/index.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        flash("Invalid email or password.")
        return redirect(url_for("home"))

    if user.status == "Blacklisted":
        flash("Your account has been blacklisted.")
        return redirect(url_for("home"))

    if user.role == "staff" and user.status != "Approved":
        flash("Your staff account is waiting for admin approval.")
        return redirect(url_for("home"))

    session["user_id"] = user.id
    session["role"] = user.role

    if user.role == "admin":
        return redirect(url_for("admin_dashboard"))
    elif user.role == "staff":
        return redirect(url_for("staff_dashboard"))
    return redirect(url_for("user_dashboard"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for("register"))

        new_user = User(
            name=request.form["name"],
            age=request.form["age"],
            email=email,
            password=request.form["password"],
            mobile=request.form["mobile"],
            address=request.form["address"],
            role="user",
            status="Approved"
        )

        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please login.")
        return redirect(url_for("home"))

    return render_template("authentication/register.html")


@app.route("/register-staff", methods=["GET", "POST"])
def register_staff():
    if request.method == "POST":
        email = request.form["email"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for("register_staff"))

        new_user = User(
            name=request.form["name"],
            age=request.form["age"],
            email=email,
            password=request.form["password"],
            mobile=request.form["mobile"],
            address=request.form["address"],
            role="staff",
            status="Pending"
        )

        db.session.add(new_user)
        db.session.commit()

        staff_profile = TrekStaff(
            trek_staff_name=new_user.name,
            phone=new_user.mobile,
            experience=request.form["experience"],
            address=new_user.address,
            emergency_contact=request.form["emergency_contact"],
            user_id=new_user.id
        )

        db.session.add(staff_profile)
        db.session.commit()

        flash("Registration successful. Wait for admin approval.")
        return redirect(url_for("home"))

    return render_template("authentication/register_staff.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))


# ADMIN

@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    total_users = User.query.filter_by(role="user").count()
    total_staff = User.query.filter_by(role="staff").count()
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()
    pending_staff = User.query.filter_by(
        role="staff", status="Pending"
    ).count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings,
        pending_staff=pending_staff
    )


@app.route("/admin/treks")
def admin_treks():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    return render_template("admin/treks.html", treks=Trek.query.all())


@app.route("/admin/treks/add", methods=["GET", "POST"])
def admin_add_trek():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    staff_list = TrekStaff.query.all()

    if request.method == "POST":
        start_date = datetime.strptime(
            request.form["start_date"], "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            request.form["end_date"], "%Y-%m-%d"
        ).date()

        staff_id = request.form.get("assigned_staff_id") or None

        new_trek = Trek(
            trek_name=request.form["trek_name"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            duration=request.form["duration"],
            available_slots=request.form["available_slots"],
            start_date=start_date,
            end_date=end_date,
            assigned_staff_id=staff_id,
            status="Pending"
        )

        db.session.add(new_trek)
        db.session.commit()
        flash("Trek added successfully.")
        return redirect(url_for("admin_treks"))

    return render_template("admin/trek_form.html", staff_list=staff_list)


@app.route("/admin/treks/<int:trek_id>/edit", methods=["GET", "POST"])
def admin_edit_trek(trek_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)
    staff_list = TrekStaff.query.all()

    if request.method == "POST":
        trek.trek_name = request.form["trek_name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = request.form["duration"]
        trek.available_slots = request.form["available_slots"]

        trek.start_date = datetime.strptime(
            request.form["start_date"], "%Y-%m-%d"
        ).date()

        trek.end_date = datetime.strptime(
            request.form["end_date"], "%Y-%m-%d"
        ).date()

        trek.assigned_staff_id = request.form.get("assigned_staff_id") or None
        trek.status = request.form["status"]

        db.session.commit()
        flash("Trek updated successfully.")
        return redirect(url_for("admin_treks"))

    return render_template(
        "admin/trek_form.html",
        trek=trek,
        staff_list=staff_list
    )


@app.route("/admin/treks/<int:trek_id>/delete", methods=["POST"])
def admin_delete_trek(trek_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted.")
    return redirect(url_for("admin_treks"))


@app.route("/admin/treks/<int:trek_id>/assign-staff", methods=["GET", "POST"])
def admin_assign_staff(trek_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    staff_list = TrekStaff.query.join(User).filter(
        User.status == "Approved"
    ).all()

    if request.method == "POST":
        trek.assigned_staff_id = request.form["staff_id"]
        db.session.commit()

        flash("Staff assigned successfully.")
        return redirect(url_for("admin_treks"))

    return render_template(
        "admin/assign_staff.html",
        trek=trek,
        staff_list=staff_list
    )


@app.route("/admin/staff")
def admin_staff():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    return render_template(
        "admin/staff.html",
        staff_list=User.query.filter_by(role="staff").all()
    )


@app.route("/admin/staff/<int:user_id>/approve", methods=["POST"])
def admin_approve_staff(user_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    staff = User.query.get_or_404(user_id)
    staff.status = "Approved"
    db.session.commit()

    flash("Staff approved.")
    return redirect(url_for("admin_staff"))


@app.route("/admin/staff/<int:user_id>/blacklist", methods=["POST"])
def admin_blacklist_staff(user_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    staff = User.query.get_or_404(user_id)
    staff.status = "Blacklisted"
    db.session.commit()

    flash("Staff blacklisted.")
    return redirect(url_for("admin_staff"))


@app.route("/admin/users")
def admin_users():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    return render_template(
        "admin/users.html",
        users_list=User.query.filter_by(role="user").all()
    )


@app.route("/admin/users/<int:user_id>/blacklist", methods=["POST"])
def admin_blacklist_user(user_id):
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    user = User.query.get_or_404(user_id)
    user.status = "Blacklisted"
    db.session.commit()

    flash("User blacklisted.")
    return redirect(url_for("admin_users"))


@app.route("/admin/bookings")
def admin_bookings():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("home"))

    return render_template(
        "admin/bookings.html",
        bookings=Booking.query.all()
    )


# USER

@app.route("/user/dashboard")
def user_dashboard():
    if "user_id" not in session or session["role"] != "user":
        return redirect(url_for("home"))

    user = User.query.get(session["user_id"])
    open_treks = Trek.query.filter_by(status="Open").count()
    my_bookings = Booking.query.filter_by(
        user_id=session["user_id"],
        booking_status="Booked"
    ).count()

    return render_template(
        "user/dashboard.html",
        user=user,
        open_treks=open_treks,
        my_bookings=my_bookings
    )


@app.route("/user/treks")
def user_treks():
    if "user_id" not in session or session["role"] != "user":
        return redirect(url_for("home"))

    return render_template(
        "user/treks.html",
        treks=Trek.query.filter_by(status="Open").all()
    )


@app.route("/user/treks/<int:trek_id>")
def user_trek_detail(trek_id):
    if "user_id" not in session or session["role"] != "user":
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    booking = Booking.query.filter_by(
        user_id=session["user_id"],
        trek_id=trek.id,
        booking_status="Booked"
    ).first()

    return render_template(
        "user/trek_detail.html",
        trek=trek,
        already_booked=bool(booking)
    )


@app.route("/user/treks/<int:trek_id>/book", methods=["POST"])
def user_book_trek(trek_id):
    if "user_id" not in session or session["role"] != "user":
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    if trek.status != "Open":
        flash("This trek is not open for booking.")
        return redirect(url_for("user_trek_detail", trek_id=trek.id))

    if trek.available_slots <= 0:
        flash("No slots available.")
        return redirect(url_for("user_trek_detail", trek_id=trek.id))

    existing_booking = Booking.query.filter_by(
        user_id=session["user_id"],
        trek_id=trek.id,
        booking_status="Booked"
    ).first()

    if existing_booking:
        flash("You have already booked this trek.")
        return redirect(url_for("user_trek_detail", trek_id=trek.id))

    new_booking = Booking(
        user_id=session["user_id"],
        trek_id=trek.id,
        booking_status="Booked",
        payment_status="Pending"
    )

    trek.available_slots -= 1
    db.session.add(new_booking)
    db.session.commit()

    flash("Trek booked successfully.")
    return redirect(url_for("user_bookings"))


@app.route("/user/bookings")
def user_bookings():
    if "user_id" not in session or session["role"] != "user":
        return redirect(url_for("home"))

    return render_template(
        "user/bookings.html",
        bookings=Booking.query.filter_by(
            user_id=session["user_id"]
        ).all()
    )


@app.route("/user/bookings/<int:booking_id>/cancel", methods=["POST"])
def user_cancel_booking(booking_id):
    if "user_id" not in session or session["role"] != "user":
        return redirect(url_for("home"))

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != session["user_id"]:
        return redirect(url_for("user_bookings"))

    if booking.booking_status == "Booked":
        booking.booking_status = "Cancelled"
        booking.trek.available_slots += 1
        db.session.commit()
        flash("Booking cancelled successfully.")

    return redirect(url_for("user_bookings"))


@app.route("/user/profile", methods=["GET", "POST"])
def user_profile():
    if "user_id" not in session or session["role"] != "user":
        return redirect(url_for("home"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        email = request.form["email"]

        existing_user = User.query.filter(
            User.email == email,
            User.id != user.id
        ).first()

        if existing_user:
            flash("Email already registered.")
            return redirect(url_for("user_profile"))

        user.name = request.form["name"]
        user.age = request.form["age"]
        user.email = email
        user.mobile = request.form["mobile"]
        user.address = request.form["address"]

        password = request.form["password"]
        if password:
            user.password = password

        db.session.commit()
        flash("Profile updated successfully.")
        return redirect(url_for("user_profile"))

    return render_template("user/profile.html", user=user)


# STAFF

@app.route("/staff/dashboard")
def staff_dashboard():
    if "user_id" not in session or session["role"] != "staff":
        return redirect(url_for("home"))

    staff = TrekStaff.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not staff:
        return redirect(url_for("home"))

    treks = Trek.query.filter_by(assigned_staff_id=staff.id).all()
    trek_counts = {
        trek.id: Booking.query.filter_by(
            trek_id=trek.id,
            booking_status="Booked"
        ).count()
        for trek in treks
    }

    return render_template(
        "staff/dashboard.html",
        staff=staff,
        treks=treks,
        trek_counts=trek_counts
    )


@app.route("/staff/treks/<int:trek_id>", methods=["GET", "POST"])
def staff_trek_detail(trek_id):
    if "user_id" not in session or session["role"] != "staff":
        return redirect(url_for("home"))

    staff = TrekStaff.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not staff:
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != staff.id:
        flash("This trek is not assigned to you.")
        return redirect(url_for("staff_dashboard"))

    booked_count = Booking.query.filter_by(
        trek_id=trek.id,
        booking_status="Booked"
    ).count()

    if request.method == "POST":
        trek.available_slots = request.form["available_slots"]
        trek.status = request.form["status"]
        db.session.commit()

        flash("Trek updated successfully.")
        return redirect(url_for("staff_trek_detail", trek_id=trek.id))

    return render_template(
        "staff/trek_form.html",
        trek=trek,
        booked_count=booked_count
    )


@app.route("/staff/treks/<int:trek_id>/participants")
def staff_trek_participants(trek_id):
    if "user_id" not in session or session["role"] != "staff":
        return redirect(url_for("home"))

    staff = TrekStaff.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not staff:
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != staff.id:
        flash("This trek is not assigned to you.")
        return redirect(url_for("staff_dashboard"))

    bookings = Booking.query.filter_by(
        trek_id=trek.id,
        booking_status="Booked"
    ).all()

    return render_template(
        "staff/participants.html",
        trek=trek,
        bookings=bookings
    )


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)