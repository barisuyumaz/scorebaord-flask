from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User, GameState
from .extensions import db
from flask_login import login_required

routes = Blueprint('routes', __name__)

#Register route---
from werkzeug.security import generate_password_hash
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Bu kullanıcı adı zaten alınmış.')
            return redirect(url_for('routes.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

#Login route---
from flask_login import login_user
from werkzeug.security import check_password_hash
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Giriş başarılı!')
            return redirect(url_for('routes.dashboard'))  # Henüz yoksa sonra ekleyeceğiz
        else:
            flash('Kullanıcı adı veya şifre hatalı.')

    return render_template('login.html')

#Logout route---
from flask_login import logout_user
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yapıldı.')
    return redirect(url_for('routes.login'))

#Index route---
from flask_login import current_user
@routes.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    else:
        return redirect(url_for('routes.login'))

#Dashboard route---
from flask_login import login_required
@routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
#---

#####################################################################

#Manage, Scoreboard routes---
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from .extensions import db, socketio
from .models import GameState
from datetime import datetime, timedelta
from flask_socketio import emit

# Bellek içi zaman kontrolü
start_time = None
time_offset = timedelta()
timer_running = False
#Scoreboard route---
@routes.route('/scoreboard')
def scoreboard():
    state = GameState.query.first()
    return render_template('scoreboard.html', state=state)

#Mage route---
@routes.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    global start_time, time_offset, timer_running

    state = GameState.query.first()
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_scores':
            state.team1_name = request.form.get('team1_name', state.team1_name)
            state.team2_name = request.form.get('team2_name', state.team2_name)
            state.team1_score = int(request.form.get('team1_score', state.team1_score))
            state.team2_score = int(request.form.get('team2_score', state.team2_score))
            db.session.commit()
            socketio.emit('update_data', _get_state_payload(state))

        elif action == 'start_timer':
            start_time = datetime.utcnow()
            timer_running = True
            socketio.emit('start_timer', {'start': True})

        elif action == 'stop_timer':
            if start_time:
                time_offset += datetime.utcnow() - start_time
            timer_running = False
            socketio.emit('stop_timer', {'start': False})

        elif action == 'set_time':
            minute = int(request.form.get('minute', 0))
            second = int(request.form.get('second', 0))
            time_offset = timedelta(minutes=minute, seconds=second)
            if timer_running:
                start_time = datetime.utcnow()
            socketio.emit('update_time', {'minute': minute, 'second': second})

        db.session.commit()

    return render_template('manage.html', state=state)

#Timer arrangements---
@socketio.on('get_time')
def handle_time_request():
    global start_time, time_offset, timer_running

    if timer_running and start_time:
        elapsed = datetime.utcnow() - start_time
    else:
        elapsed = timedelta()

    total = time_offset + elapsed
    emit('update_time', {
        'minute': total.seconds // 60,
        'second': total.seconds % 60
    })

#Score arrangements---
def _get_state_payload(state):
    return {
        'team1_name': state.team1_name,
        'team2_name': state.team2_name,
        'team1_score': state.team1_score,
        'team2_score': state.team2_score
    }