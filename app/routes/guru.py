from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import User, Student, RiasecResult, Recommendation
from app import db
from sqlalchemy import func

guru_bp = Blueprint('guru', __name__)

@guru_bp.route('/guru')
@login_required
def dashboard_guru():
    if current_user.role != 'guru':
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
        # Prioritaskan filter dari User.kelas, tapi cek juga Student.kelas sebagai fallback jika perlu
        # Namun agar konsisten dengan display, kita filter di User.kelas dulu karena itu data utama sekarang
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
        "dashboard_guru.html",
        siswa_list=siswa_list,
        pagination=pagination,
        siswa_sudah_tes=sudah_tes,
        siswa_belum_tes=belum_tes,
        total_siswa=total_siswa,
        distribusi=distribusi_list,
        # Kirim balik filter values ke template
        filters={
            'riasec': filter_riasec,
            'kelas': filter_kelas,
            'paket': filter_paket,
            'nama': filter_nama
        }
    )

@guru_bp.route('/guru/detail_siswa/<int:user_id>')
@login_required
def detail_siswa(user_id):
    if current_user.role != 'guru':
        return redirect(url_for('auth.login'))
        
    user = User.query.get_or_404(user_id)
    student = Student.query.filter_by(id_user=user.id).first()
    
    # Default values
    riasec_data = None
    rekom_data = None
    rapor_data = None
    
    if student:
        riasec_result = RiasecResult.query.filter_by(id_student=student.id).first()
        if riasec_result:
            riasec_data = {
                'top3': riasec_result.top3,
                'skor': {
                    'R': riasec_result.skor_R,
                    'I': riasec_result.skor_I,
                    'A': riasec_result.skor_A,
                    'S': riasec_result.skor_S,
                    'E': riasec_result.skor_E,
                    'C': riasec_result.skor_C
                }
            }
            
        rekom = Recommendation.query.filter_by(id_student=student.id).first()
        if rekom:
            rekom_data = rekom.paket_prediksi
            
        from app.models import ReportScore
        rapor = ReportScore.query.filter_by(id_student=student.id).first()
        if rapor:
            rapor_data = {
                'Biologi': rapor.biologi,
                'Fisika': rapor.fisika,
                'Kimia': rapor.kimia,
                'Matematika': rapor.matematika,
                'Ekonomi': rapor.ekonomi,
                'Sosiologi': rapor.sosiologi
            }

    return render_template(
        "detail_siswa_guru.html",
        user=user,
        student=student,
        riasec_data=riasec_data,
        rekom_data=rekom_data,
        rapor_data=rapor_data
    )
