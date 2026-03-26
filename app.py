from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Cycle
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smartcycle-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ── Helper functions ──────────────────────────────────────────────

def calculate_predictions(last_period, cycle_length):
    """Calculate next period, ovulation day, and fertile window."""
    next_period = last_period + timedelta(days=cycle_length)
    ovulation_day = last_period + timedelta(days=cycle_length - 14)
    fertile_start = ovulation_day - timedelta(days=5)
    fertile_end = ovulation_day + timedelta(days=1)
    
    # Determine current phase
    today = datetime.today().date()
    days_since = (today - last_period).days
    
    if days_since < 0:
        phase = "Pre-cycle"
    elif days_since <= 5:
        phase = "Menstrual Phase"
    elif days_since <= cycle_length - 16:
        phase = "Follicular Phase"
    elif days_since <= cycle_length - 12:
        phase = "Ovulation Phase"
    elif days_since <= cycle_length:
        phase = "Luteal Phase"
    else:
        phase = "Cycle Complete"
    
    return {
        'next_period': next_period,
        'ovulation_day': ovulation_day,
        'fertile_start': fertile_start,
        'fertile_end': fertile_end,
        'phase': phase,
        'days_until_next': (next_period - today).days
    }

def send_email_reminder(to_email, subject, body):
    """Send email reminder (configure SMTP settings before use)."""
    # NOTE: Configure these with your email credentials
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SENDER_EMAIL = 'your-email@gmail.com'
    SENDER_PASSWORD = 'your-app-password'
    
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ── Routes ────────────────────────────────────────────────────────

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken!', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    cycles = Cycle.query.filter_by(user_id=current_user.id).order_by(Cycle.last_period.desc()).all()
    predictions = None
    
    if cycles:
        latest = cycles[0]
        predictions = calculate_predictions(latest.last_period, latest.cycle_length)
        predictions['mood'] = latest.mood
        predictions['notes'] = latest.notes
    
    return render_template('dashboard.html', cycles=cycles, predictions=predictions)

@app.route('/log_cycle', methods=['GET', 'POST'])
@login_required
def log_cycle():
    if request.method == 'POST':
        last_period = datetime.strptime(request.form['last_period'], '%Y-%m-%d').date()
        cycle_length = int(request.form['cycle_length'])
        mood = request.form.get('mood', '')
        notes = request.form.get('notes', '')
        
        if cycle_length < 21 or cycle_length > 35:
            flash('Cycle length should be between 21 and 35 days.', 'warning')
            return redirect(url_for('log_cycle'))
        
        cycle = Cycle(
            user_id=current_user.id,
            last_period=last_period,
            cycle_length=cycle_length,
            mood=mood,
            notes=notes
        )
        db.session.add(cycle)
        db.session.commit()
        
        flash('Cycle logged successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('log_cycle.html')

@app.route('/history')
@login_required
def history():
    cycles = Cycle.query.filter_by(user_id=current_user.id).order_by(Cycle.last_period.desc()).all()
    
    # Add predictions to each cycle for display
    history_data = []
    for c in cycles:
        pred = calculate_predictions(c.last_period, c.cycle_length)
        history_data.append({
            'cycle': c,
            'predictions': pred
        })
    
    return render_template('history.html', history_data=history_data)

@app.route('/delete_cycle/<int:cycle_id>')
@login_required
def delete_cycle(cycle_id):
    cycle = Cycle.query.get_or_404(cycle_id)
    if cycle.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(cycle)
    db.session.commit()
    flash('Cycle entry deleted.', 'info')
    return redirect(url_for('history'))

# ── Initialize DB ─────────────────────────────────────────────────

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
