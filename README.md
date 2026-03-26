# SmartCycle: Menstrual Monitoring Web App

A web-based menstrual cycle tracking and reminder system built with Python & Flask.

**By:** Final Year College Project

## Features
- User Registration & Login
- Log period dates & cycle length
- Auto-calculate next period, ovulation day, fertile window
- Four-phase tracking (Menstrual, Follicular, Ovulation, Luteal)
- Mood & notes logging
- Cycle history with predictions
- Email reminders (configurable)

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open in browser
# http://127.0.0.1:5000
```

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap 5
- **Auth:** Flask-Login with password hashing

## Project Structure
```
SmartCycle/
├── app.py              # Main application & routes
├── models.py           # Database models (User, Cycle)
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── log_cycle.html
│   └── history.html
└── static/
    └── style.css       # Custom styles
```

## Email Reminders
To enable email reminders, update the SMTP settings in `app.py`:
- `SENDER_EMAIL`: Your Gmail address
- `SENDER_PASSWORD`: App-specific password (not your regular password)
