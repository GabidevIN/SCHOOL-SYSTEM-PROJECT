import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_migrate import Migrate


#Flask app initialization
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

#class for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 
    profile_picture = db.Column(db.String(120), default=False) 
    full_name = db.Column(db.String(120), nullable=True) 
    address = db.Column(db.String(255), nullable=True)
    contact_number = db.Column(db.String(15), nullable=True) 
    courses = db.Column(db.String(120), nullable=True) 
    section = db.Column(db.String(120), nullable=True)
    year = db.Column(db.String(120), nullable=True)
    supporting_document = db.Column(db.String(120), nullable=True) 
    is_new = db.Column(db.Boolean, default=True) 
    approved = db.Column(db.Boolean, default=False) 
    is_teacher = db.Column(db.Boolean, default=False)  
    note = db.Column(db.String(255), nullable=True)  
    
    
    

    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()
#class for RegistrationRequest for the extra registration
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
#class for the grades for students
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Float, nullable=False)
    student = db.relationship('User', backref=db.backref('grades', lazy=True))

    def __repr__(self):
        return f'<Grade {self.subject} - {self.grade}>'
with app.app_context():
    db.create_all()
#upload folder for the profile picture and supporting document
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#set routes for default
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', defaults={'source': 'normal'}, methods=['GET', 'POST'])
@app.route('/login/<source>', methods=['GET', 'POST'])
def login(source):
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

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')

            print(f"User {user.username} is_admin: {user.is_admin}")
            print(f"Session user_id: {session['user_id']}")
            print(f"Session username: {session['username']}")

            if user.is_admin:
                return redirect(url_for('admin_home'))
            elif user.is_teacher:
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('main'))
            
        flash('Invalid username or password!', 'danger')
        print("REDIRECTION ERROR")
        return redirect(url_for('login', source='failed'))

    # Choose appropriate template based on source
    if source == 'success': template = 'login3.html' 
    elif source == 'normal': template = 'login.html'
    else: template = 'login2.html'
    return render_template(template)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if username or email already exists
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user_exists or email_exists:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('login', source='failed'))

        # Hash the password and save the registration request
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        registration_request = RegistrationRequest(username=username, email=email, password=hashed_password)

        try:
            db.session.add(registration_request)
            db.session.commit()
            flash('Registration request submitted! Please wait for approval.', 'success')
            return redirect(url_for('login', source='success'))
        except Exception as e:
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('login', source='failed'))

    return render_template('register.html')
#route for the main page
@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('login', source='failed'))

    if request.method == 'POST':
        # Save the note
        note = request.form.get('note')
        if note:
            user.note = note
            db.session.commit()
            flash('Note saved successfully!', 'success')

    return render_template('studentFile/main.html', user=user)
#route for the profile page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('login', source='failed'))

    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.address = request.form.get('address')
        user.contact_number = request.form.get('contact_number')

        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = filename

        # Handle supporting document upload
        if 'supporting_document' in request.files:
            file = request.files['supporting_document']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.supporting_document = filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('studentFile/profileinfo.html', user=user)
#route for the admin profile page
@app.route('/profile/admin', methods=['GET', 'POST'])
def profile_admin():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin: 
        flash('User not found!', 'danger')
        return redirect(url_for('main'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        address = request.form.get('address')
        contact_number = request.form.get('contact_number')
        
        if full_name:
            user.full_name = full_name
        if address:
            user.address = address
        if contact_number:
            user.contact_number = contact_number

        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = filename

        # Handle supporting document upload
        if 'supporting_document' in request.files:
            file = request.files['supporting_document']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.supporting_document = filename
                
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile_admin'))
    return render_template('adminFile/profileinfo_admin.html', user=user)

#route for the admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    # Fetch pending and completed registration requests
    registration_requests = RegistrationRequest.query.filter_by(approved=True).all()
    completed_registrations = RegistrationRequest.query.filter_by(approved=True).all()

    return render_template('adminFile/admin_dashboard.html', registration_requests=registration_requests, completed_registrations=completed_registrations)
#route for the admin home page
@app.route('/admin/home')
def admin_home():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    users = User.query.all()
    return render_template('adminFile/admin_home.html', users=users) 


#route for the all logout
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
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

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

#for admin that decline the registration
@app.route('/admin/decline/<int:request_id>', methods=['POST'])
def decline_registration(request_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    registration_request = db.session.get(RegistrationRequest, request_id)
    if registration_request:
        db.session.delete(registration_request)
        db.session.commit()
        flash(f'Registration request for {registration_request.username} has been declined.', 'success')
    else:
        flash('Registration request not found.', 'danger')

    return redirect(url_for('admin_dashboard'))


# Route to handle the promotion of students
from sqlalchemy import or_

@app.route('/promote_all_students', methods=['POST'])
def promote_all_students():
    new_level = request.form.get('new_level')
    selected_students_ids = request.form.getlist('selected_students')  # Get the selected student IDs

    if new_level and selected_students_ids:
        # Get the selected students by their IDs
        users_to_promote = User.query.filter(User.id.in_(selected_students_ids)).all()

        for user in users_to_promote:
            user.section = new_level

        db.session.commit()

        flash(f'Selected students have been promoted to {new_level}!', 'success')
    else:
        flash('No level or students selected!', 'danger')

    return redirect(url_for('admin_sections'))







# Route to render the ADMIN sections page with users
@app.route('/admin/sections')
@app.route('/admin/sections/<section>')
def admin_sections(section=None):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    users = User.query.all()

    if section == 'EE':
        template = 'adminFile/admin_section_EE.html'
    elif section == 'IE':
        template = 'adminFile/admin_section_IE.html'
    else:
        template = 'adminFile/admin_section.html'

    return render_template(template, users=users)

# Route to render the TEACHER sections page with users
@app.route('/teacher/sections')
@app.route('/teacher/sections/<section>')
def teacher_sections(section=None):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_teacher:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    users = User.query.all()

    if section == 'EE':
        template = 'teacherFile/teacher_section_EE.html'
    elif section == 'IE':
        template = 'teacherFile/teacher_section_IE.html'
    else:
        template = 'teacherFile/teacher_section.html'

    return render_template(template, users=users)

#list of all users for admin  
@app.route('/users')
def list_users():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    users = User.query.all()
    return render_template('adminFile/user_list.html', users=users)

@app.route('/admin/update-user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or not admin_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    user = db.session.get(User, user_id)
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('list_users'))

    # INPUT IN THE OPTIONS
    new_year = request.form.get('year')
    new_section = request.form.get('section')

    # UPDATE THE YEAR
    if new_year:
        user.year = new_year
        flash(f'{user.username}\'s year has been updated to {new_year}!', 'success')

    # UPDATE SECTION
    if new_section:
        user.section = new_section
        flash(f'{user.username}\'s section has been updated to {new_section}!', 'success')

    # SAVE CHANGES (SAVE BOTTON BOI)
    db.session.commit()

    return redirect(url_for('list_users'))

#route from admin to promote a user to teacher // PROMOTE TEACHER TO NOH??
@app.route('/admin/promote/<int:user_id>', methods=['POST'])
def promote_to_teacher(user_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    admin_user = db.session.get(User, session['user_id'])
    if not admin_user or not admin_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    user = db.session.get(User, user_id)
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Promote the user to a teacher
    user.is_teacher = True
    db.session.commit()
    flash(f'{user.username} has been promoted to Teacher!', 'success')
    return redirect(url_for('admin_dashboard'))



#route for the extra registration page from the login page
@app.route('/extra-registration', methods=['GET', 'POST'])
def extra_registration():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

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
#for the student that have pending registration
@app.route('/ex_register')
def ex_register():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    # Fetch the registration request
    extra_details = RegistrationRequest.query.filter_by(id=session['user_id']).first()
    if not extra_details:
        flash('No registration details found!', 'danger')
        return redirect(url_for('main'))
    last_user = db.session.get(User, session['user_id'])


    return render_template('register_complete.html', extra_details=extra_details, last_user=last_user)
#upload the profile picture for the user
@app.route('/upload-picture', methods=['GET', 'POST'])
def upload_picture():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

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


#grades system for the students
#list of subjects
SUBJECTS = ["Physics 1","Chemistry","CAD","Physical Education 1"]


#grades for the admin to show
@app.route('/admin/grades', methods=['GET'])
def admin_grades():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    students = User.query.all()
    return render_template('adminFile/admin_grades.html', students=students)


@app.route('/admin/grades/<int:student_id>', methods=['GET'])
def admin_grades_for_student(student_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    student = User.query.get(student_id)
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('admin_grades'))

    grades = Grade.query.filter_by(student_id=student.id).all()

    return render_template('adminFile/admin_grades.html', student=student, grades=grades)


#admin add grades for the students
@app.route('/admin/add-grades/<int:student_id>', methods=['GET', 'POST'])
def add_grades(student_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

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

    return render_template('adminFile/add_grades.html', student=student, subjects=SUBJECTS)


#admin view grades for the students
@app.route('/admin/view-grades', methods=['GET'])
def admin_view_grades():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))
    students_with_grades = db.session.query(User).join(Grade).distinct().all()
    grades = Grade.query.all()

    return render_template('adminFile/admin_view_grades.html', students=students_with_grades, grades=grades)


#student show their grades
@app.route('/student/grades', methods=['GET'])
def student_grades():
    if 'user_id' not in session:
        flash('Access denied! Please log in.', 'danger')
        return redirect(url_for('login', source='failed'))

    student = db.session.get(User, session['user_id'])
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('login', source='failed'))

    grades = Grade.query.filter_by(student_id=student.id).all()

    return render_template('studentFile/student_grades.html', student=student, grades=grades)


#student show their subjects
@app.route('/student/sub', methods=['GET'])
def student_subjects():
    if 'user_id' not in session:
        flash('Access denied! Please log in.', 'danger')
        return redirect(url_for('login', source='failed'))

    student = db.session.get(User, session['user_id'])
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('login', source='failed'))

    grades = Grade.query.filter_by(student_id=student.id).all()

    return render_template('studentFile/student_subjects.html', student=student, grades=grades)


#extra about page for the student
@app.route('/student/about')
def abouts():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('login', source='failed'))

    print("Rendering about.html") 
    return render_template('studentFile/about.html', user=user)


#extra about page for the admin
@app.route('/admin/about')
def admin_about():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))
    
    is_admin = db.session.get(User, session['user_id'])
    if not is_admin or not is_admin.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))
    
    print("Rendering about.html")
    return render_template('adminFile/about_admin.html', user=is_admin)

    
#Teacher
#teaacher dashboard for the teacher
@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    user = db.session.get(User, session['user_id'])
    if not user or not user.is_teacher:  # Check for teacher role
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    students = User.query.all()  # Fetch all students
    return render_template('teacherFile/teacher_dashboard.html', students=students)


#teacher grades for the students
@app.route('/teacher/grades', methods=['GET'])
def teacher_grades():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_teacher:  # Check for teacher role
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    students = User.query.all()
    return render_template('teacherFile/teacher_grades.html', students=students)


#teacher grades for the students
@app.route('/teacher/grades/<int:student_id>', methods=['GET'])
def teacher_grades_for_student(student_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_teacher:  # Check for teacher role
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    student = User.query.get(student_id)
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('teacher_grades'))

    grades = Grade.query.filter_by(student_id=student.id).all()

    return render_template('teacherFile/teacher_grades.html', student=student, grades=grades)


#teacher add grades for the students
@app.route('/teacher/add-grades/<int:student_id>', methods=['GET', 'POST'])
def teacher_add_grades(student_id):
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_teacher:  # Check for teacher role
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    student = User.query.get(student_id)
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('teacher_grades'))

    if request.method == 'POST':
        for subject in SUBJECTS:
            grade_value = request.form.get(subject)
            if grade_value:
                existing_grade = Grade.query.filter_by(student_id=student.id, subject=subject).first()
                if existing_grade:
                    existing_grade.grade = float(grade_value)  # Update
                else:
                    # Add new grade
                    new_grade = Grade(
                        student_id=student.id,
                        subject=subject,
                        semester=request.form.get('semester', 1),
                        grade=float(grade_value)
                    )
                    db.session.add(new_grade)
        db.session.commit()
        flash('Grades added/updated successfully!', 'success')
        return redirect(url_for('teacher_grades'))

    return render_template('teacherFile/add_grades_teacher.html', student=student, subjects=SUBJECTS)


@app.route('/teacher/view-grades', methods=['GET'])
def teacher_view_grades():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    current_user = db.session.get(User, session['user_id'])
    if not current_user or not current_user.is_teacher:  # Check for teacher role
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    students_with_grades = db.session.query(User).join(Grade).distinct().all()
    grades = Grade.query.all()

    return render_template('teacher_view_grades.html', students=students_with_grades, grades=grades)


#teacher view grades for the students
@app.route('/teacher/profile', methods=['GET', 'POST'])
def teacher_profile():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    user = db.session.get(User, session['user_id'])
    if not user or not user.is_teacher:  # Ensure the user is a teacher
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))

    if request.method == 'POST':
        # Handle profile updates
        full_name = request.form.get('full_name')
        address = request.form.get('address')
        contact_number = request.form.get('contact_number')

        # Update user details
        if full_name:
            user.full_name = full_name
        if address:
            user.address = address
        if contact_number:
            user.contact_number = contact_number

        # Handle file upload for profile picture
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = filename

        # Handle supporting document upload
        if 'supporting_document' in request.files:
            file = request.files['supporting_document']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.supporting_document = filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('teacher_profile'))

    return render_template('teacherFile/teacher_profile.html', user=user)
    

#route for the teacher about page
@app.route('/teacher/about')
def teacher_about():
    if 'user_id' not in session:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))
    
    is_teacher = db.session.get(User, session['user_id'])
    if not is_teacher or not is_teacher.is_teacher:
        flash('Access denied!', 'danger')
        return redirect(url_for('login', source='failed'))
    
    print("Rendering about.html")
    return render_template('teacherFile/teacher_about.html', user=is_teacher)

if __name__ == '__main__':
    app.run(debug=True, port=8000)