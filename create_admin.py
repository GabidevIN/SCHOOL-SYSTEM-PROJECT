from main import app, db, User
from werkzeug.security import generate_password_hash

def create_admin():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print('Admin user already exists!')
    else:
        admin = User(
            username='admin1', 
            email='admin@ex', # FOR CREATING ADMIN email
            password=generate_password_hash('admin', method='pbkdf2:sha256'), # ADMIN PASSWORD change "admin"
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully!')

if __name__ == '__main__':
    with app.app_context():
        create_admin()
