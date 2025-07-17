# 🏀 Real-Time Scoreboard Web App

A real-time scoreboard web application built with Flask and Socket.IO for managing and displaying live match data.

---

## 🚀 Features

- User authentication (Referee or Official roles)
- Start, pause, and update live match timer
- Real-time updates for team names, scores and period
- Instant data broadcasting with WebSocket (Socket.IO)
- Separate views for scoreboard and management panel
- Timer continues globally regardless of user sessions

---

## 🖼️ Screenshots
<img width="1764" height="1562" alt="scoreboard-project-sss" src="https://github.com/user-attachments/assets/c72af7eb-08d4-49fa-83c5-d15183ae6370" />

---

## 🛠️ Technologies Used

- Python 3.x
- Flask
- Flask-SocketIO
- Flask-Login
- SQLAlchemy
- PostgreSQL

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/barisuyumaz/scoreboard-app.git
cd scoreboard-app

# 2. Create a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the application
flask run
