from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Student, RiasecResult, Recommendation
from app import db

guru_bp = Blueprint('guru', __name__)

@guru_bp.route('/guru')
@login_required
def dashboard_guru():
    if current_user.role != 'guru':
        return redirect(url_for('auth.login'))

    students = Student.query.all()
    siswa_list = []
    distribusi = {"Paket 1": 0, "Paket 2": 0, "Paket 3": 0}
    sudah_tes = 0
    belum_tes = 0
    for s in students:
        result = RiasecResult.query.filter_by(id_student=s.id).first()
        rekom = Recommendation.query.filter_by(id_student=s.id).first()
        if result:
            sudah_tes += 1
            kode_riasec = result.top3 or "-"
        else:
            belum_tes += 1
            kode_riasec = "-"
        paket = rekom.paket_prediksi if rekom else "-"
        if paket in distribusi:
            distribusi[paket] += 1
        siswa_list.append({
            "nama": s.nama,
            "nisn": s.nisn,
            "kode_riasec": kode_riasec,
            "paket_rekomendasi": paket,
            "id": s.id
        })
    distribusi_list = [distribusi["Paket 1"], distribusi["Paket 2"], distribusi["Paket 3"]]
    return render_template(
        "dashboard_guru.html",
        siswa_list=siswa_list,
        siswa_sudah_tes=sudah_tes,
        siswa_belum_tes=belum_tes,
        distribusi=distribusi_list
    )