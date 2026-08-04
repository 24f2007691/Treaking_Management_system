from flask import Flask, render_template, request, session, redirect, url_for, flash
from models import *
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking_app_database.sqlite3"
app.secret_key = "secretkey"

db.init_app(app)

# Home route

@app.route("/")
def home():
    return render_template("authentication/index.html")

# Login route

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(
        email=email,
        password=password
    ).first()

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

    else:
        return redirect(url_for("user_dashboard"))

#register user route

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

# register staff route

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

# ADMIN DASHBOARD

@app.route("/admin/dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    total_users = User.query.filter_by(role="user").count()
    total_staff = User.query.filter_by(role="staff").count()
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()

    pending_staff = User.query.filter_by(
        role="staff",
        status="Pending"
    ).count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings,
        pending_staff=pending_staff
    )

# Treks Admin Route

@app.route("/admin/treks")
def admin_treks():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    treks = Trek.query.all()

    return render_template("admin/treks.html", treks=treks)

# Add Trek Admin Route

@app.route("/admin/treks/add", methods=["GET", "POST"])
def admin_add_trek():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    staff_list = TrekStaff.query.all()

    if request.method == "POST":

        start_date = datetime.strptime(
            request.form["start_date"], "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            request.form["end_date"], "%Y-%m-%d"
        ).date()

        new_trek = Trek(
            trek_name=request.form["trek_name"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            duration=request.form["duration"],
            available_slots=request.form["available_slots"],
            start_date=start_date,
            end_date=end_date,
            assigned_staff_id=request.form["assigned_staff_id"],
            status="Pending"
        )

        db.session.add(new_trek)
        db.session.commit()

        return redirect(url_for("admin_treks"))

    return render_template(
        "admin/trek_form.html",
        staff_list=staff_list
    )

# Edit Trek Admin Route

@app.route("/admin/treks/<int:trek_id>/edit", methods=["GET", "POST"])
def admin_edit_trek(trek_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
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

        trek.assigned_staff_id = request.form["assigned_staff_id"]
        trek.status = request.form["status"]

        db.session.commit()

        flash("Trek updated successfully.")

        return redirect(url_for("admin_treks"))

    return render_template(
        "admin/trek_form.html",
        trek=trek,
        staff_list=staff_list
    )

# Delete Trek Admin Route

@app.route("/admin/treks/<int:trek_id>/delete", methods=["POST"])
def admin_delete_trek(trek_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted.")

    return redirect(url_for("admin_treks"))

# Assign Staff to Trek Admin Route

@app.route("/admin/treks/<int:trek_id>/assign-staff", methods=["GET", "POST"])
def admin_assign_staff(trek_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    trek = Trek.query.get_or_404(trek_id)

    staff_list = TrekStaff.query.join(User).filter(
        User.status == "Approved"
    ).all()

    if request.method == "POST":

        staff_id = request.form["staff_id"]

        trek.assigned_staff_id = staff_id

        db.session.commit()

        flash("Staff assigned successfully.")

        return redirect(url_for("admin_treks"))

    return render_template(
        "admin/assign_staff.html",
        trek=trek,
        staff_list=staff_list
    )

# Staff Management Admin Route

@app.route("/admin/staff")
def admin_staff():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    staff_list = User.query.filter_by(role="staff").all()

    return render_template(
        "admin/staff.html",
        staff_list=staff_list
    )

# Approval staff

@app.route("/admin/staff/<int:user_id>/approve", methods=["POST"])
def admin_approve_staff(user_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    staff = User.query.get_or_404(user_id)

    staff.status = "Approved"

    db.session.commit()

    flash("Staff approved.")

    return redirect(url_for("admin_staff"))

# Blacklist staff 

@app.route("/admin/staff/<int:user_id>/blacklist", methods=["POST"])
def admin_blacklist_staff(user_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    staff = User.query.get_or_404(user_id)

    staff.status = "Blacklisted"

    db.session.commit()

    flash("Staff blacklisted.")

    return redirect(url_for("admin_staff"))

# user management adimn

@app.route("/admin/users")
def admin_users():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    users_list = User.query.filter_by(role="user").all()

    return render_template(
        "admin/users.html",
        users_list=users_list
    )

# blacklisting user 

@app.route("/admin/users/<int:user_id>/blacklist", methods=["POST"])
def admin_blacklist_user(user_id):

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    user = User.query.get_or_404(user_id)

    user.status = "Blacklisted"

    db.session.commit()

    flash("User blacklisted.")

    return redirect(url_for("admin_users"))

# display bookings for admin

@app.route("/admin/bookings")
def admin_bookings():

    if "user_id" not in session:
        return redirect(url_for("home"))

    if session["role"] != "admin":
        return redirect(url_for("home"))

    bookings = Booking.query.all()

    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )


# Create database tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)