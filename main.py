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
app.config['MYSQL_PASSWORD'] = '131418'  
app.config['MYSQL_DB'] = 'school_system_project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:131418@localhost/school_system_project'  # Update this line with the correct password // PASSWORD OF UR DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    db = SQLAlchemy(app)
    mysql = MySQL(app)
    migrate = Migrate(app, db)
except Exception as e:
    print(f"Error connecting to the database: {e}")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 
    profile_picture = db.Column(db.String(120), default='default.jpg') 
    full_name = db.Column(db.String(120), nullable=True)  # New
    address = db.Column(db.String(255), nullable=True)  # New
    contact_number = db.Column(db.String(15), nullable=True)  # New
    courses = db.Column(db.String(120), nullable=True)  # New
    
    supporting_document = db.Column(db.String(120), nullable=True)  # New
    is_new = db.Column(db.Boolean, default=True)  # new
    approved = db.Column(db.Boolean, default=False)  #new
    
    

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
    full_name = db.Column(db.String(120), nullable=True)  # New
    address = db.Column(db.String(255), nullable=True)  # New
    contact_number = db.Column(db.String(15), nullable=True)  #new
    supporting_document = db.Column(db.String(120), nullable=True) # New
    is_new = db.Column(db.Boolean, default=True) # New
    course = db.Column(db.String(120), nullable=True)  # New
    BSCPE = db.Column(db.String(80), nullable=False)
    BSIE = db.Column(db.String(80), nullable=False)
    BSEE = db.Column(db.String(80), nullable=False)
     

    def __repr__(self):
        return f'<RegistrationRequest {self.username}>'

class Grade(db.Model): #pota wala pa to
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Float, nullable=False)
    student = db.relationship('User', backref=db.backref('grades', lazy=True))

    def __repr__(self):
        return f'<Grade {self.subject} - {self.grade}>'
    

    
UPLOAD_FOLDER = 'static/uploads'  # Folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with app.app_context():
    db.create_all()
    

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        registration_request = RegistrationRequest.query.filter_by(email=email).first()
        print(f"Registration Request: {registration_request}")

        user = User.query.filter_by(email=email).first()
        print(f"User: {user}")

        if registration_request and registration_request.is_new:
            print(f"Redirecting to extra registration for {registration_request.username}")
            session['user_id'] = registration_request.id 
            return redirect(url_for('extra_registration'))

        # Check
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')

            print(f"User {user.username} is_admin: {user.is_admin}")
            print(f"Session user_id: {session['user_id']}")
            print(f"Session username: {session['username']}")

            # Redirect
            if user.is_admin:
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('main'))
            
        flash('Invalid username or password!', 'danger')
        print("REDIRECTION ERROR")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(f"Password: {password}, Confirm Password: {confirm_password}")  # Debugging

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')  # Ensure this is correct

    return render_template('register.html')  # Ensure this is correct

@app.route('/main')
def main():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('login'))

    print("Rendering main.html") 
    return render_template('main.html', user=user)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('main'))

    if request.method == 'POST':

        user.full_name = request.form.get('full_name')
        user.address = request.form.get('address')
        user.contact_number = request.form.get('contact_number')

        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.supporting_document = filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profileinfo.html', user=user)

@app.route('/profile/admin', methods=['GET', 'POST'])
def profile_admin():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('main'))

    if request.method == 'POST':
        # Update user information
        user.full_name = request.form.get('full_name')
        user.address = request.form.get('address')
        user.contact_number = request.form.get('contact_number')

        # Handle file upload for supporting document
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.supporting_document = filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profileinfo_admin.html', user=user)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    # Fetch pending and completed registration requests
    registration_requests = RegistrationRequest.query.filter_by(approved=True).all()
    completed_registrations = RegistrationRequest.query.filter_by(approved=True).all()

    return render_template('admin_dashboard.html', registration_requests=registration_requests, completed_registrations=completed_registrations)

@app.route('/admin/home')
def admin_home():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('admin_home.html', users=users) 

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

    registration_request = RegistrationRequest.query.get(request_id)
    if registration_request:
        # Create
        new_user = User(
            username=registration_request.username,
            email=registration_request.email,
            password=registration_request.password,
            full_name=registration_request.full_name,
            address=registration_request.address,
            contact_number=registration_request.contact_number,
            supporting_document=registration_request.supporting_document,
            courses = registration_request.course,

        )
        db.session.add(new_user)
        db.session.delete(registration_request)  # Remove
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


#list ng mga bulgago 
@app.route('/users')
def list_users():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('user_list.html', users=users)



@app.route('/extra-registration', methods=['GET', 'POST'])
def extra_registration():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    registration_request = RegistrationRequest.query.filter_by(id=session['user_id']).first()
    if not registration_request:
        flash('Access denied!', 'danger')
        return redirect(url_for('main'))

    if registration_request.approved:
        flash('You have already completed your registration!', 'info')
        return redirect(url_for('ex_register'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        address = request.form.get('address')
        contact_number = request.form.get('contact_number')
        selected_course = request.form.get('course')  
        flash(f'You selected: {selected_course}', 'success')

        # File upload
        if 'file' not in request.files:
            flash('No file part!', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file!', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            registration_request.full_name = full_name
            registration_request.address = address
            registration_request.contact_number = contact_number
            registration_request.course = selected_course 
            registration_request.supporting_document = filename
            registration_request.approved = True  #approved
            registration_request.is_new = True  #
            db.session.commit()

            flash('Extra registration details submitted successfully!', 'success')
            return redirect(url_for('ex_register'))

    courses = ['BSCPE', 'BSIE', 'BSEE']
    return render_template('ex_reg.html', registration_request=registration_request, courses=courses)

@app.route('/ex_register')
def ex_register():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    # Fetch the registration request
    extra_details = RegistrationRequest.query.filter_by(id=session['user_id']).first()
    if not extra_details:
        flash('No registration details found!', 'danger')
        return redirect(url_for('main'))
    last_user = db.session.get(User, session['user_id'])


    return render_template('register_complete.html', extra_details=extra_details, last_user=last_user)

@app.route('/upload-picture', methods=['GET', 'POST'])
def upload_picture():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('main'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part!', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file!', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.profile_picture = filename  
            db.session.commit()
            flash('Profile picture uploaded successfully!', 'success')
            return redirect(url_for('main'))

    return render_template('upload_picture.html', user=user)

@app.route('/about')
def about():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('login'))

    return render_template('about.html', user=user) 

#grades na to

SUBJECTS = [
    "Physics 1",
    "Chemistry",
    "CAD",
    "Physical Education 1"
]

@app.route('/admin/grades', methods=['GET'])
def admin_grades():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    students = User.query.all()
    return render_template('admin_grades.html', students=students)

@app.route('/admin/grades/<int:student_id>', methods=['GET'])
def admin_grades_for_student(student_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    student = User.query.get(student_id)
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('admin_grades'))

    grades = Grade.query.filter_by(student_id=student.id).all()

    return render_template('admin_grades.html', student=student, grades=grades)

@app.route('/admin/add-grades/<int:student_id>', methods=['GET', 'POST'])
def add_grades(student_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    student = User.query.get(student_id)
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('admin_grades'))

    if request.method == 'POST':
        for subject in SUBJECTS:
            grade_value = request.form.get(subject)
            if grade_value:
                existing_grade = Grade.query.filter_by(student_id=student.id, subject=subject).first()
                if existing_grade:
                    existing_grade.grade = float(grade_value)  # Update
                else:
                    # new grade
                    new_grade = Grade(
                        student_id=student.id,
                        subject=subject,
                        semester=request.form.get('semester', 1),
                        grade=float(grade_value)
                    )
                    db.session.add(new_grade)
        db.session.commit()
        flash('Grades added/updated successfully!', 'success')
        return redirect(url_for('admin_grades'))

    return render_template('add_grades.html', student=student, subjects=SUBJECTS)

@app.route('/admin/view-grades', methods=['GET'])
def admin_view_grades():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))
    students_with_grades = db.session.query(User).join(Grade).distinct().all()
    grades = Grade.query.all()

    return render_template('admin_view_grades.html', students=students_with_grades, grades=grades)

@app.route('/student/grades', methods=['GET'])
def student_grades():
    if 'user_id' not in session:
        flash('Access denied! Please log in.', 'danger')
        return redirect(url_for('login'))

    student = db.session.get(User, session['user_id'])
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('login'))

    grades = Grade.query.filter_by(student_id=student.id).all()

    return render_template('student_grades.html', student=student, grades=grades)

@app.route('/student/sub', methods=['GET'])
def student_subjects():
    if 'user_id' not in session:
        flash('Access denied! Please log in.', 'danger')
        return redirect(url_for('login'))

    student = db.session.get(User, session['user_id'])
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('login'))

    grades = Grade.query.filter_by(student_id=student.id).all()

    return render_template('student_subjects.html', student=student, grades=grades)

@app.route('/student/about', methods=['GET'])
def about_us():
    if 'user_id' not in session:
        flash('Access denied! Please log in.', 'danger')
        return redirect(url_for('login'))

    student = db.session.get(User, session['user_id'])
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('login'))

    grades = Grade.query.filter_by(student_id=student.id).all()

    return render_template('TESTINGWAVES.html', student=student, grades=grades)

if __name__ == '__main__':
    app.run(debug=True, port=8000)