# 🩸 SmartCycle — Period & Fertility Tracker

SmartCycle is a web-based menstrual cycle tracking application built with Flask. It helps users log their periods, predict upcoming cycles, identify fertile windows, and track ovulation — all through a clean, intuitive interface.

---

## ✨ Features

- 🔐 **User Authentication** — Secure signup/login with hashed passwords
- 📅 **Cycle Logging** — Record period start dates and cycle lengths
- 🔮 **Period Prediction** — Automatically calculates the next expected period
- 🥚 **Ovulation Tracking** — Pinpoints ovulation day based on cycle data
- 💚 **Fertile Window** — Highlights the 6-day fertility window
- 📊 **Cycle Phase Detection** — Identifies current phase (Menstrual, Follicular, Ovulation, Luteal)
- 📱 **Responsive Design** — Works seamlessly on desktop and mobile

---

## 🛠️ Tech Stack

| Layer        | Technology                     |
|-------------|-------------------------------|
| **Backend**  | Python, Flask                 |
| **Database** | SQLite via Flask-SQLAlchemy   |
| **Auth**     | Flask-Login, Werkzeug hashing |
| **Frontend** | HTML, CSS, Jinja2 Templates   |

---

## 📁 Project Structure

```
SmartCycle/
├── app.py              # Main application (routes, logic, config)
├── requirements.txt    # Python dependencies
├── instance/
│   └── smartcycle.db   # SQLite database (auto-generated)
├── templates/
│   ├── base.html       # Base layout template
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── dashboard.html  # Main dashboard with predictions
│   └── log_cycle.html  # Cycle logging form
├── static/
│   └── style.css       # Custom styles
└── README.md           # This file
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/AnshK07/SmartCycle.git
cd SmartCycle

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. Open in browser
# Navigate to http://127.0.0.1:5000
```

---

## 🔑 Core Logic

| Calculation       | Formula                                    |
|-------------------|--------------------------------------------|
| **Next Period**   | `last_period_date + cycle_length`          |
| **Ovulation Day** | `next_period_date - 14 days`               |
| **Fertile Window**| `ovulation_day - 5` to `ovulation_day`     |

### Cycle Phases
- **Menstrual** — Days 1–5 from period start
- **Follicular** — Day 6 to ovulation
- **Ovulation** — Ovulation day ± 1
- **Luteal** — Post-ovulation to next period

---

## 📸 Screenshots

| Screen | Preview |
|--------|---------|
| Login Page | <img width="1849" height="649" alt="image" src="https://github.com/user-attachments/assets/0f42588b-af0e-4d03-8758-732f2a2bd4d1" />

| Screen | Preview |
|--------|---------|
| Register Page | <img width="1852" height="712" alt="image" src="https://github.com/user-attachments/assets/644ad99b-3fd6-4af2-ae5a-46c896043161" />

| Screen | Preview |
|--------|---------|
| Dashboard | <img width="1936" height="905" alt="image" src="https://github.com/user-attachments/assets/0668c05a-0fb4-46e6-9393-0dd150fb4d0d" />

---

## 🔒 Security

- Passwords are hashed using **Werkzeug** (never stored in plaintext)
- Session-based authentication via **Flask-Login**
- SQL injection prevention through **SQLAlchemy ORM**

---
