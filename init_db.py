from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    
    # Check if admin exists
    admin_user = User.query.filter_by(username = 'admin').first()

    if not admin_user:
        hashed_pw = generate_password_hash('admin123')
        admin = User(username = 'admin', password = hashed_pw, role = 'admin', is_active = True, is_approved = True)
        db.session.add(admin)
        db.session.commit()

        print("Admin created [username: admin, password: admin123]")

    else:
        print("Admin already exists.")
