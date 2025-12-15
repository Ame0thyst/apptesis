from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def home():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            if user.role == "admin":
                return redirect(url_for('admin.dashboard_admin'))
            elif user.role == "guru":
                return redirect(url_for('guru.dashboard_guru'))
            else:
                return redirect(url_for('siswa.dashboard_siswa'))
        else:
            flash("Login gagal. Cek username/password!")
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))