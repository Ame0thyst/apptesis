from flask import Blueprint, render_template, redirect, url_for, send_file
from flask_login import login_required, current_user
from app import db
from app.models import User, Student, RiasecResult, Recommendation
import io
import csv

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def dashboard_admin():
    # Jumlah total siswa & guru
    total_siswa = Student.query.count()
    total_guru = User.query.filter_by(role="guru").count()

    # Jumlah siswa yang sudah tes (ada riasec_result)
    siswa_sudah_tes = RiasecResult.query.count()

    # Ambil semua siswa
    siswa_list = Student.query.all()

    # Data untuk tabel siswa
    data_siswa = []
    for s in siswa_list:
        nisn = s.nisn
        nama = s.nama
        # Status tes
        status_tes = "Sudah Tes" if RiasecResult.query.filter_by(id_student=s.id).first() else "Belum Tes"
        # Paket rekomendasi
        rekom = Recommendation.query.filter_by(id_student=s.id).first()
        paket = rekom.paket_prediksi if rekom else "-"
        data_siswa.append({
            "nama": nama,
            "nisn": nisn,
            "status_tes": status_tes,
            "paket": paket
        })

    # Pie Chart data
    total_rekom = Recommendation.query.count()
    paket1 = Recommendation.query.filter_by(paket_prediksi="Paket 1").count()
    paket2 = Recommendation.query.filter_by(paket_prediksi="Paket 2").count()
    paket3 = Recommendation.query.filter_by(paket_prediksi="Paket 3").count()
    paket1_pct = round(100 * paket1 / total_rekom, 1) if total_rekom else 0
    paket2_pct = round(100 * paket2 / total_rekom, 1) if total_rekom else 0
    paket3_pct = round(100 * paket3 / total_rekom, 1) if total_rekom else 0

    return render_template(
        'dashboard_admin.html',
        total_siswa=total_siswa,
        total_guru=total_guru,
        siswa_sudah_tes=siswa_sudah_tes,
        data_siswa=data_siswa,
        paket1_pct=paket1_pct,
        paket2_pct=paket2_pct,
        paket3_pct=paket3_pct
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