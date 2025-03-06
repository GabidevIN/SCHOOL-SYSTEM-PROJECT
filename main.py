from flask import Flask
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '131418'
app.config['MYSQL_DB'] = 'school_system_project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:131418@localhost/school_system_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mysql = MySQL(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) 
    
    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()


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
            return redirect(url_for('main'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)  # Debugging statement
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Debugging statements
        print(f"Username: {username}, Email: {email}, Password: {password}")
        
        # Check if user or email already exists
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        
        # Debugging statements
        print(f"User exists: {user_exists}, Email exists: {email_exists}")
        
        if user_exists:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))
        
        if email_exists:
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error: {e}")  # Debugging statement
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('login.html')

# SUCCESSFUL LOGIN (PENDING IF/ELSE)
@app.route('/home')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    username = session.get('username', 'Guest')
    return render_template('main.html', username=username)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
