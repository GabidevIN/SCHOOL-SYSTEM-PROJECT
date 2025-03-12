from flask import Flask
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '131418'  # Update this line with the correct password // PASSWORD OF UR DB // 121318 -- GAB
app.config['MYSQL_DB'] = 'school_system_project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:131418@localhost/school_system_project'  # Update this line with the correct password // PASSWORD OF UR DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mysql = MySQL(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) 
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()


class RegistrationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<RegistrationRequest {self.username}>'

with app.app_context():
    db.create_all()

@app.route('/home')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    username = session.get('username', 'Guest')
    return render_template('main.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')

            print(f"User {user.username} is_admin: {user.is_admin}")
            print(f"Session user_id: {session['user_id']}")
            print(f"Session username: {session['username']}")

            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('main'))
        else:
            flash('Invalid username or password!', 'danger')

            print("REDIRECTION ERROR") # ERROR CHECKING
            
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        
        if user_exists or email_exists:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        registration_request = RegistrationRequest(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(registration_request)
            db.session.commit()
            flash('Registration request submitted! Please wait for approval.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    # Debug statement to check session data
    print(f"Admin Dashboard accessed by user_id: {session['user_id']}")

    registration_requests = RegistrationRequest.query.all()
    return render_template('admin_dashboard.html', registration_requests=registration_requests)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/admin/approve/<int:request_id>', methods=['POST'])
def approve_registration(request_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    registration_request = db.session.get(RegistrationRequest, request_id)
    if registration_request:
        new_user = User(
            username=registration_request.username,
            email=registration_request.email,
            password=registration_request.password
        )
        db.session.add(new_user)
        db.session.delete(registration_request)
        db.session.commit()
        flash(f'Registration request for {new_user.username} has been approved.', 'success')
    else:
        flash('Registration request not found.', 'danger')

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/decline/<int:request_id>', methods=['POST'])
def decline_registration(request_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    registration_request = db.session.get(RegistrationRequest, request_id)
    if registration_request:
        db.session.delete(registration_request)
        db.session.commit()
        flash(f'Registration request for {registration_request.username} has been declined.', 'success')
    else:
        flash('Registration request not found.', 'danger')

    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)