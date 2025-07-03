from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from models import db, User, Team, Fixture, CantinaReservation, Sponsor
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from datetime import timedelta, datetime
from functools import wraps

main_bp = Blueprint('main', __name__)

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        uid = get_jwt_identity()
        user = User.query.get(uid)
        if user.role != 'administrador':
            flash('Acceso solo para administradores')
            return redirect(url_for('main.dashboard'))
        return fn(*args, **kwargs)
    return wrapper

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if User.query.filter_by(username=username).first():
            flash('Usuario existente')
            return redirect(url_for('main.register'))
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso, ahora puedes iniciar sesión')
        return redirect(url_for('main.login'))
    return render_template('register.html')


@main_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
            resp = redirect(url_for('main.dashboard'))
            set_access_cookies(resp, access_token)
            session['user_id'] = user.id
            return resp
        flash('Credenciales inválidas')
        return redirect(url_for('main.login'))
    return render_template('login.html')


@main_bp.route('/logout')
@jwt_required()
def logout():
    resp = redirect(url_for('main.index'))
    unset_jwt_cookies(resp)
    session.clear()
    return resp


@main_bp.route('/dashboard')
@jwt_required()
def dashboard():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    return render_template('dashboard.html', user=user)


@main_bp.route('/teams', methods=['GET', 'POST'])
@jwt_required()
def teams():
    if request.method == 'POST':
        name = request.form['name']
        sport = request.form['sport']
        category = request.form['category']
        team = Team(name=name, sport=sport, category=category)
        db.session.add(team)
        db.session.commit()
        flash('Equipo creado')
        return redirect(url_for('main.teams'))
    data = Team.query.all()
    return render_template('teams.html', teams=data)


@main_bp.route('/teams/delete/<int:team_id>', methods=['POST'])
@admin_required
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    flash('Equipo eliminado')
    return redirect(url_for('main.teams'))


@main_bp.route('/fixtures', methods=['GET', 'POST'])
def fixtures():
    data = Fixture.query.all()
    if not data:
        class Dummy:
            pass
        f1 = Dummy(); f1.id=1; f1.home_team=Dummy(); f1.home_team.name='Renault FC'; f1.away_team=Dummy(); f1.away_team.name='Peugeot United'; f1.date=datetime(2025,7,10,18,0); f1.score_home=2; f1.score_away=1
        f2 = Dummy(); f2.id=2; f2.home_team=Dummy(); f2.home_team.name='Citroën Stars'; f2.away_team=Dummy(); f2.away_team.name='Fiat Power'; f2.date=datetime(2025,7,11,20,0); f2.score_home=0; f2.score_away=0
        data = [f1, f2]
    return render_template('fixtures.html', fixtures=data)


@main_bp.route('/results')
def results():
    data = Fixture.query.filter(Fixture.score_home!=None).all()
    if not data:
        class Dummy:
            pass
        f1 = Dummy(); f1.id=1; f1.home_team=Dummy(); f1.home_team.name='Renault FC'; f1.away_team=Dummy(); f1.away_team.name='Peugeot United'; f1.score_home=2; f1.score_away=1
        f2 = Dummy(); f2.id=2; f2.home_team=Dummy(); f2.home_team.name='Citroën Stars'; f2.away_team=Dummy(); f2.away_team.name='Fiat Power'; f2.score_home=0; f2.score_away=0
        data = [f1, f2]
    return render_template('results.html', fixtures=data)


@main_bp.route('/cantina', methods=['GET', 'POST'])
@jwt_required()
def cantina():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        menu = request.form['menu']
        dietary_restrictions = request.form['dietary_restrictions']
        reservation = CantinaReservation(user_id=user_id, menu=menu, dietary_restrictions=dietary_restrictions)
        db.session.add(reservation)
        db.session.commit()
        flash('Reserva realizada')
        return redirect(url_for('main.cantina'))
    data = CantinaReservation.query.all()
    return render_template('cantina.html', reservations=data)


@main_bp.route('/sponsors')
def sponsors():
    data = Sponsor.query.all()
    if not data:
        class Dummy:
            pass
        s1 = Dummy(); s1.id=1; s1.name='Renault'; s1.website='https://www.renault.com'; s1.banner_url='https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Renault_2021_logo.svg/512px-Renault_2021_logo.svg.png'
        s2 = Dummy(); s2.id=2; s2.name='Peugeot'; s2.website='https://www.peugeot.com'; s2.banner_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Peugeot_Logo.svg/512px-Peugeot_Logo.svg.png'
        data = [s1, s2]
    return render_template('sponsors.html', sponsors=data)


@main_bp.route('/admin')
@admin_required
def admin_panel():
    users = User.query.all()
    teams = Team.query.all()
    fixtures = Fixture.query.all()
    sponsors = Sponsor.query.all()
    return render_template('admin_panel.html', users=users, teams=teams, fixtures=fixtures, sponsors=sponsors)
