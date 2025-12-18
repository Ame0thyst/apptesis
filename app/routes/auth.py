from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
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
        
        # Verifikasi password (mendukung Hash dan Plain Text untuk backward compatibility)
        is_valid_password = False
        if user:
            # 1. Cek Hash (Prioritas Utama)
            try:
                if check_password_hash(user.password, password):
                    is_valid_password = True
            except:
                pass
            
            # 2. Cek Plain Text (Fallback untuk data lama)
            if not is_valid_password and user.password == password:
                is_valid_password = True

        if user and is_valid_password:
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

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm', '').strip()
        nama = request.form.get('nama', '').strip()
        nisn = request.form.get('nisn', '').strip()
        kelas = request.form.get('kelas', '').strip()
        
        if not username or not password:
            flash("Username dan password wajib diisi.")
            return render_template('register.html')
        if password != confirm:
            flash("Konfirmasi password tidak cocok.")
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.")
            return render_template('register.html')
        if nisn and User.query.filter_by(nisn=nisn).first():
            flash("NISN sudah ditemukan.")
            return render_template('register.html', nisn_error=True)
        
        user = User(
            username=username,
            password=generate_password_hash(password),
            role='siswa',
            nama=nama if nama else username,
            nisn=nisn if nisn else None,
            kelas=kelas if kelas else None
        )
        db.session.add(user)
        db.session.commit()
        
        from app.models import Student
        student = Student(
            id_user=user.id,
            nama=user.nama,
            nisn=user.nisn,
            kelas=user.kelas
        )
        db.session.add(student)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('siswa.dashboard_siswa'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
