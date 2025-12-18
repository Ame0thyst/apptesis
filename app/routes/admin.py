from flask import Blueprint, render_template, redirect, url_for, send_file, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app import db
from app.models import User, Student, RiasecResult, Recommendation
from sqlalchemy import func
import io
import csv

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def dashboard_admin():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    # Ambil parameter pagination dan filter
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    filter_riasec = request.args.get('riasec', '')
    filter_kelas = request.args.get('kelas', '')
    filter_paket = request.args.get('paket', '')
    filter_nama = request.args.get('nama', '')

    # --- HITUNG STATISTIK GLOBAL (Semua Data) ---
    # Total Siswa
    total_siswa = User.query.filter_by(role='siswa').count()
    # Total Guru
    total_guru = User.query.filter_by(role='guru').count()
    
    # Siswa Sudah Tes (yang punya record RiasecResult)
    # Join: User -> Student -> RiasecResult
    sudah_tes = db.session.query(func.count(User.id))\
        .join(Student, User.id == Student.id_user)\
        .join(RiasecResult, Student.id == RiasecResult.id_student)\
        .filter(User.role == 'siswa').scalar()
        
    belum_tes = total_siswa - sudah_tes
    
    # Distribusi Paket (Paket 1, 2, 3)
    # Group by paket_prediksi
    dist_query = db.session.query(Recommendation.paket_prediksi, func.count(Recommendation.id))\
        .join(Student, Recommendation.id_student == Student.id)\
        .join(User, Student.id_user == User.id)\
        .filter(User.role == 'siswa')\
        .group_by(Recommendation.paket_prediksi).all()
        
    distribusi_dict = {"Paket 1": 0, "Paket 2": 0, "Paket 3": 0}
    for paket, count in dist_query:
        if paket in distribusi_dict:
            distribusi_dict[paket] = count
            
    distribusi_list = [distribusi_dict["Paket 1"], distribusi_dict["Paket 2"], distribusi_dict["Paket 3"]]

    # --- QUERY UTAMA UNTUK TABEL (Filtered & Paginated) ---
    # Kita perlu join table agar bisa filter
    # Base query: Pilih User, Student, RiasecResult, Recommendation
    query = db.session.query(User, Student, RiasecResult, Recommendation)\
        .outerjoin(Student, User.id == Student.id_user)\
        .outerjoin(RiasecResult, Student.id == RiasecResult.id_student)\
        .outerjoin(Recommendation, Student.id == Recommendation.id_student)\
        .filter(User.role == 'siswa')
        
    # Apply Filters
    if filter_riasec:
        query = query.filter(RiasecResult.top3.ilike(f"%{filter_riasec}%"))
        
    if filter_kelas:
        query = query.filter(User.kelas.ilike(f"%{filter_kelas}%"))
        
    if filter_paket:
        query = query.filter(Recommendation.paket_prediksi == filter_paket)

    if filter_nama:
        query = query.filter(User.nama.ilike(f"%{filter_nama}%"))

    # Sorting (Optional: by ID desc or Name asc)
    query = query.order_by(User.nama.asc())

    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    siswa_list = []
    for u, s, res, rec in pagination.items:
        # Logika prioritas data (User > Student)
        nama_siswa = u.nama if u.nama else (s.nama if s else u.username)
        nisn_siswa = u.nisn if u.nisn else (s.nisn if s else "-")
        kelas_siswa = u.kelas if u.kelas else (s.kelas if s else "-")
        
        kode_riasec = res.top3 if res else "-"
        paket = rec.paket_prediksi if rec else "-"
        
        siswa_list.append({
            "id": u.id,
            "nama": nama_siswa,
            "nisn": nisn_siswa,
            "kelas": kelas_siswa,
            "kode_riasec": kode_riasec,
            "paket_rekomendasi": paket
        })

    return render_template(
        "dashboard_admin.html",
        siswa_list=siswa_list,
        pagination=pagination,
        siswa_sudah_tes=sudah_tes,
        siswa_belum_tes=belum_tes,
        total_siswa=total_siswa,
        total_guru=total_guru,
        distribusi=distribusi_list,
        # Kirim balik filter values ke template
        filters={
            'riasec': filter_riasec,
            'kelas': filter_kelas,
            'paket': filter_paket,
            'nama': filter_nama
        }
    )

@admin_bp.route('/admin/guru')
@login_required
def guru_list():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    page = request.args.get('page', 1, type=int)
    per_page = 10
    filter_nama = request.args.get('nama', '')

    query = User.query.filter_by(role='guru')

    if filter_nama:
        query = query.filter(User.nama.ilike(f"%{filter_nama}%"))

    pagination = query.order_by(User.nama.asc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('guru_list.html', pagination=pagination, filter_nama=filter_nama)

@admin_bp.route('/admin/guru/add', methods=['GET', 'POST'])
@login_required
def add_guru():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nama = request.form.get('nama')
        nisn = request.form.get('nisn')  # NIP disimpan di kolom nisn
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validasi sederhana
        if not nama or not username or not password:
            flash('Nama, Username, dan Password harus diisi.', 'error')
            return redirect(url_for('admin.add_guru'))

        if password != confirm_password:
            flash('Password tidak cocok.', 'error')
            return redirect(url_for('admin.add_guru'))
        
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan.', 'error')
            return redirect(url_for('admin.add_guru'))

        if nisn and User.query.filter_by(nisn=nisn).first():
            flash('NIP (NISN) sudah digunakan.', 'error')
            return redirect(url_for('admin.add_guru'))

        new_guru = User(
            username=username,
            password=generate_password_hash(password),
            role='guru',
            nama=nama,
            nisn=nisn
        )
        
        try:
            db.session.add(new_guru)
            db.session.commit()
            flash('Guru berhasil ditambahkan.', 'success')
            return redirect(url_for('admin.guru_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
            return redirect(url_for('admin.add_guru'))

    return render_template('add_guru.html')

@admin_bp.route('/admin/guru/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_guru(id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
        
    guru = User.query.get_or_404(id)
    if guru.role != 'guru':
        flash('Data tidak ditemukan atau bukan guru.', 'error')
        return redirect(url_for('admin.guru_list'))
        
    if request.method == 'POST':
        nama = request.form.get('nama')
        nisn = request.form.get('nisn')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not nama or not username:
            flash('Nama dan Username wajib diisi.', 'error')
            return redirect(url_for('admin.edit_guru', id=id))
            
        # Check unique username (exclude self)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != guru.id:
            flash('Username sudah digunakan user lain.', 'error')
            return redirect(url_for('admin.edit_guru', id=id))
            
        # Check unique nisn (exclude self)
        if nisn:
            existing_nisn = User.query.filter_by(nisn=nisn).first()
            if existing_nisn and existing_nisn.id != guru.id:
                flash('NIP sudah digunakan user lain.', 'error')
                return redirect(url_for('admin.edit_guru', id=id))
        
        guru.nama = nama
        guru.nisn = nisn
        guru.username = username
        
        if password:
            if password != confirm_password:
                flash('Password baru tidak cocok.', 'error')
                return redirect(url_for('admin.edit_guru', id=id))
            guru.password = generate_password_hash(password)
            
        try:
            db.session.commit()
            flash('Data guru berhasil diperbarui.', 'success')
            return redirect(url_for('admin.guru_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal memperbarui: {str(e)}', 'error')
            return redirect(url_for('admin.edit_guru', id=id))
            
    return render_template('edit_guru.html', guru=guru)

@admin_bp.route('/admin/guru/delete/<int:id>', methods=['POST'])
@login_required
def delete_guru(id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
        
    guru = User.query.get_or_404(id)
    if guru.role != 'guru':
        flash('Data tidak valid.', 'error')
        return redirect(url_for('admin.guru_list'))
        
    try:
        db.session.delete(guru)
        db.session.commit()
        flash('Guru berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal menghapus: {str(e)}', 'error')
        
    return redirect(url_for('admin.guru_list'))

@admin_bp.route('/admin/import', methods=['GET', 'POST'])
@login_required
def import_data():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Tidak ada file yang diunggah.', 'error')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('Tidak ada file yang dipilih.', 'error')
            return redirect(request.url)
            
        if file and (file.filename.endswith('.csv') or file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
            try:
                import pandas as pd
                
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file, dtype=str)
                else:
                    df = pd.read_excel(file, dtype=str)
                
                # Normalisasi nama kolom (lowercase)
                df.columns = [c.lower() for c in df.columns]
                
                required_cols = ['nama', 'nisn', 'kelas']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    flash(f'Format file salah. Kolom wajib: {", ".join(missing_cols)} tidak ditemukan.', 'error')
                    return redirect(request.url)
                
                success_count = 0
                error_count = 0
                
                for index, row in df.iterrows():
                    try:
                        nama = str(row['nama']).strip()
                        nisn = str(row['nisn']).strip()
                        kelas = str(row['kelas']).strip()
                        
                        # Generate username & password default dari NISN
                        username = nisn
                        password = nisn
                        role = 'siswa'

                        # Override jika kolom ada di CSV
                        if 'username' in df.columns and str(row['username']) != 'nan' and str(row['username']).strip():
                            username = str(row['username']).strip()
                        
                        if 'password' in df.columns and str(row['password']) != 'nan' and str(row['password']).strip():
                            password = str(row['password']).strip()

                        if 'role' in df.columns and str(row['role']) != 'nan' and str(row['role']).strip():
                            role = str(row['role']).strip().lower()
                        
                        if not nisn or not nama:
                            continue
                            
                        # Cek duplikat NISN
                        if User.query.filter_by(nisn=nisn).first():
                            error_count += 1
                            continue
                            
                        # Cek duplikat Username
                        if User.query.filter_by(username=username).first():
                            # Jika username (NISN) sudah ada, coba tambahkan suffix atau skip
                            # Di sini kita skip saja karena NISN harus unik sebagai username siswa
                            error_count += 1
                            continue
                            
                        new_user = User(
                            username=username,
                            password=generate_password_hash(password),
                            role=role,
                            nama=nama,
                            nisn=nisn,
                            kelas=kelas
                        )
                        db.session.add(new_user)
                        db.session.flush() # Flush untuk dapat ID user
                        
                        new_student = Student(
                            id_user=new_user.id,
                            nama=nama,
                            nisn=nisn,
                            kelas=kelas
                        )
                        db.session.add(new_student)
                        success_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        print(f"Error importing row {index}: {e}")
                        continue
                        
                db.session.commit()
                
                if success_count > 0:
                    flash(f'Berhasil mengimport {success_count} data siswa. Gagal/Duplikat: {error_count}.', 'success')
                else:
                    flash(f'Tidak ada data yang diimport. Semua data ({error_count}) mungkin duplikat atau error.', 'error')
                    
                return redirect(url_for('admin.dashboard_admin'))
                
            except Exception as e:
                flash(f'Terjadi kesalahan saat memproses file: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Format file tidak didukung. Gunakan CSV atau Excel.', 'error')
            return redirect(request.url)
            
    return render_template('import_data.html')

@admin_bp.route('/admin/download-template')
@login_required
def download_template():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
        
    output = io.BytesIO()
    import pandas as pd
    
    # Membuat template dataframe kosong
    df = pd.DataFrame(columns=['Nama', 'NISN', 'Kelas'])
    
    # Contoh data (optional)
    # df.loc[0] = ['Siswa Contoh', '1234567890', 'XII IPA 1']
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Template Siswa')
        
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='template_import_siswa.xlsx'
    )

# Optional: Download CSV
@admin_bp.route('/admin/download-csv')
@login_required
def download_csv():
    siswa_list = Student.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Nama', 'NISN', 'Status Tes', 'Paket Rekomendasi'])
    for s in siswa_list:
        status_tes = "Sudah Tes" if RiasecResult.query.filter_by(id_student=s.id).first() else "Belum Tes"
        rekom = Recommendation.query.filter_by(id_student=s.id).first()
        paket = rekom.paket_prediksi if rekom else "-"
        writer.writerow([s.nama, s.nisn, status_tes, paket])
    output.seek(0)
    return send_file(
        io.BytesIO(output.read().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='data_siswa.csv'
    )