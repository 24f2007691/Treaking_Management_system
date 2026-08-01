from app import app
from models import db,User

with app.app_context():
    db.create_all()

    admin=User.query.filter_by(role="admin").first()

    if admin is None:
        admin=User(
            name="Sujal Pareek",
            age=22,
            email="admin@gmail.com",
            password="admin123",
            mobile="9999999999",
            address="Katihar Bihar",
            role="admin",
            status="Active"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully")
    else:
        print("Admin already exists")









        