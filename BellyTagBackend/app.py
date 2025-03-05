from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'doctor' or 'patient'

# Routes
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Find the user in the database
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:
        login_user(user)
        if user.role == 'doctor':
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('patient_screen'))
    else:
        flash('Login Failed. Check your username and/or password')
        return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'doctor':
        return redirect(url_for('home'))
    
    # Get all patients for the doctor
    patients = User.query.filter_by(role='patient').all()
    return render_template('dashboard.html', patients=patients)

@app.route('/patient/<int:patient_id>')
@login_required
def patient_screen(patient_id):
    patient = User.query.get_or_404(patient_id)
    return render_template('patient_screen.html', patient=patient)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()  # Create the database (first time only)
    app.run(debug=True)
