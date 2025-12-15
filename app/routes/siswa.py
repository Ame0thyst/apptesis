import os
import joblib
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user, logout_user
from datetime import datetime
from app import db
from app.models import Student, RiasecQuestion, RiasecAnswer, RiasecResult, ReportScore, Recommendation

siswa_bp = Blueprint('siswa', __name__)

SOAL_PER_HALAMAN = 7

# Landing page route
@siswa_bp.route('/')
def landing_page():
    return render_template('landing.html')

@siswa_bp.route('/siswa')
@login_required
def dashboard_siswa():
    # hanya siswa boleh mengakses dashboard siswa
    if getattr(current_user, 'role', None) != 'siswa':
        return redirect(url_for('auth.login'))

    # cari record student (relasi ke user)
    student = Student.query.filter_by(id_user=current_user.id).first()

    # Ambil nama siswa jika ada, fallback ke username
    if student and getattr(student, 'nama', None):
        student_name = student.nama
    else:
        # fallback: user punya username (models.User punya field username)
        student_name = getattr(current_user, 'username', None) or 'Nama Siswa'

    # cek keberadaan hasil untuk setiap langkah
    riasec_done = False
    rapor_done = False
    rekom_done = False

    if student:
        riasec_done = RiasecResult.query.filter_by(id_student=student.id).first() is not None
        rapor_done = ReportScore.query.filter_by(id_student=student.id).first() is not None
        rekom_done = Recommendation.query.filter_by(id_student=student.id).first() is not None

    completed = sum([riasec_done, rapor_done, rekom_done])
    percent = int((completed / 3) * 100) if completed >= 0 else 0

    # status teks singkat (opsional untuk ditampilkan)
    if percent == 100:
        status = "Selesai"
    elif percent == 0:
        status = "Belum mengerjakan"
    else:
        status = "Sedang mengerjakan"

    return render_template(
        'dashboard_siswa.html',
        student_name=student_name,
        percent=percent,
        status=status,
        riasec_done=riasec_done,
        rapor_done=rapor_done,
        rekom_done=rekom_done
    )

# LOGOUT route
@siswa_bp.route('/logout')
@login_required
def logout():
    logout_user()
    # redirect ke halaman login (publik) supaya tidak memicu login_required
    return redirect(url_for('auth.login'))
    # jika ingin redirect ke landing/public page, gunakan:
    # return redirect(url_for('siswa.landing_page'))

@siswa_bp.route('/tes_riasec', methods=['GET', 'POST'])
@login_required
def tes_riasec():
    student = Student.query.filter_by(id_user=current_user.id).first()
    if not student:
        flash("Data siswa tidak ditemukan.")
        return redirect(url_for('siswa.dashboard_siswa'))

    total_soal = RiasecQuestion.query.count()
    SOAL_PER_HALAMAN = 7
    total_page = (total_soal + SOAL_PER_HALAMAN - 1) // SOAL_PER_HALAMAN

    if request.method == 'POST':
        page = int(request.form.get("page", 1))
        nav = request.form.get("nav", "next")
        pertanyaan_ids = request.form.getlist("pertanyaan_ids")
        # Simpan jawaban
        for qid in pertanyaan_ids:
            val = request.form.get(f"jawaban_{qid}")
            if val is not None:
                existing = RiasecAnswer.query.filter_by(id_student=student.id, id_question=int(qid)).first()
                if existing:
                    existing.skor = 1 if val == "YA" else 0
                else:
                    db.session.add(RiasecAnswer(id_student=student.id, id_question=int(qid), skor=1 if val == "YA" else 0))
        db.session.commit()

        # Jika di halaman terakhir dan klik "Selanjutnya", proses hasil dan redirect
        if nav == "next" and page == total_page:
            answers = RiasecAnswer.query.filter_by(id_student=student.id).all()
            skor = {'R':0, 'I':0, 'A':0, 'S':0, 'E':0, 'C':0}
            for a in answers:
                q = RiasecQuestion.query.get(a.id_question)
                if q and q.dimensi in skor:
                    skor[q.dimensi] += a.skor
            sorted_dimensi = sorted(skor, key=lambda k: skor[k], reverse=True)
            top3 = ''.join(sorted_dimensi[:3])
            result = RiasecResult.query.filter_by(id_student=student.id).first()
            if result:
                result.skor_R = skor['R']
                result.skor_I = skor['I']
                result.skor_A = skor['A']
                result.skor_S = skor['S']
                result.skor_E = skor['E']
                result.skor_C = skor['C']
                result.top3 = top3
            else:
                result = RiasecResult(
                    id_student=student.id,
                    skor_R=skor['R'],
                    skor_I=skor['I'],
                    skor_A=skor['A'],
                    skor_S=skor['S'],
                    skor_E=skor['E'],
                    skor_C=skor['C'],
                    top3=top3
                )
                db.session.add(result)
            db.session.commit()
            return redirect(url_for('siswa.hasil_riasec'))

        # Navigasi halaman
        if nav == "next" and page < total_page:
            page += 1
        elif nav == "prev":
            page -= 1
        if page < 1: page = 1
        if page > total_page: page = total_page
    else:
        page = int(request.args.get("page", 1))
        if page < 1: page = 1
        if page > total_page: page = total_page

    pertanyaan_query = RiasecQuestion.query.order_by(RiasecQuestion.id).offset((page-1)*SOAL_PER_HALAMAN).limit(SOAL_PER_HALAMAN)
    pertanyaan_list = [{"id": q.id, "text": q.pertanyaan} for q in pertanyaan_query]

    jawaban = {}
    for q in pertanyaan_list:
        ans = RiasecAnswer.query.filter_by(id_student=student.id, id_question=q["id"]).first()
        if ans:
            jawaban[q["id"]] = "YA" if ans.skor == 1 else "TIDAK"

    progress = page / total_page if total_page > 0 else 0

    return render_template(
        'tes_riasec.html',
        pertanyaan_list=pertanyaan_list,
        page=page,
        total_page=total_page,
        progress=progress,
        jawaban=jawaban
    )

@siswa_bp.route('/hasil_riasec')
@login_required
def hasil_riasec():
    student = Student.query.filter_by(id_user=current_user.id).first()
    result = RiasecResult.query.filter_by(id_student=student.id).first() if student else None
    if result:
        skor_list = [result.skor_R, result.skor_I, result.skor_A, result.skor_S, result.skor_E, result.skor_C]
        top3 = result.top3 or "-"
    else:
        skor_list = [0,0,0,0,0,0]
        top3 = "-"
    return render_template('hasil_riasec.html', skor_list=skor_list, top3=top3)

@siswa_bp.route('/input_nilai', methods=['GET', 'POST'])
@login_required
def input_nilai():
    student = Student.query.filter_by(id_user=current_user.id).first()
    if request.method == 'POST':
        # Ambil nilai dari form
        biologi = request.form.get('biologi')
        fisika = request.form.get('fisika')
        kimia = request.form.get('kimia')
        matematika = request.form.get('matematika')
        ekonomi = request.form.get('ekonomi')
        sosiologi = request.form.get('sosiologi')
        # Cek apakah sudah ada data untuk student ini
        rapor = ReportScore.query.filter_by(id_student=student.id).first()
        if rapor:
            rapor.biologi = biologi
            rapor.fisika = fisika
            rapor.kimia = kimia
            rapor.matematika = matematika
            rapor.ekonomi = ekonomi
            rapor.sosiologi = sosiologi
        else:
            rapor = ReportScore(
                id_student=student.id,
                biologi=biologi,
                fisika=fisika,
                kimia=kimia,
                matematika=matematika,
                ekonomi=ekonomi,
                sosiologi=sosiologi
            )
            db.session.add(rapor)
        db.session.commit()
        return redirect(url_for('siswa.hasil_rekomendasi'))
    return render_template('input_nilai.html')

@siswa_bp.route('/hasil_rekomendasi')
@login_required
def hasil_rekomendasi():
    student = Student.query.filter_by(id_user=current_user.id).first()
    hasil_riasec = RiasecResult.query.filter_by(id_student=student.id).first() if student else None

    # Ambil nilai rapor dari database
    rapor = ReportScore.query.filter_by(id_student=student.id).first() if student else None
    if not hasil_riasec:
        flash("Silakan selesaikan Tes RIASEC terlebih dahulu.")
        return redirect(url_for('siswa.tes_riasec'))
    if not rapor:
        flash("Silakan isi nilai rapor terlebih dahulu.")
        return redirect(url_for('siswa.input_nilai'))
    if rapor:
        nilai_rapor = {
            'biologi': int(rapor.biologi) if rapor.biologi else 0,
            'fisika': int(rapor.fisika) if rapor.fisika else 0,
            'kimia': int(rapor.kimia) if rapor.kimia else 0,
            'matematika': int(rapor.matematika) if rapor.matematika else 0,
            'ekonomi': int(rapor.ekonomi) if rapor.ekonomi else 0,
            'sosiologi': int(rapor.sosiologi) if rapor.sosiologi else 0
        }
    else:
        nilai_rapor = {
            'biologi': 0,
            'fisika': 0,
            'kimia': 0,
            'matematika': 0,
            'ekonomi': 0,
            'sosiologi': 0
        }

    # Siapkan input fitur untuk model (urutkan sesuai training!)
    riasec_scores = [
        hasil_riasec.skor_R if hasil_riasec else 0,
        hasil_riasec.skor_I if hasil_riasec else 0,
        hasil_riasec.skor_A if hasil_riasec else 0,
        hasil_riasec.skor_S if hasil_riasec else 0,
        hasil_riasec.skor_E if hasil_riasec else 0,
        hasil_riasec.skor_C if hasil_riasec else 0
    ]
    rapor_scores = [
        nilai_rapor['biologi'],
        nilai_rapor['fisika'],
        nilai_rapor['kimia'],
        nilai_rapor['matematika'],
        nilai_rapor['ekonomi'],
        nilai_rapor['sosiologi']
    ]
    model_input = riasec_scores + rapor_scores

    xgb_path = os.path.join(current_app.root_path, 'utils', 'model_rekomendasi_xgb.pkl')
    rf_path = os.path.join(current_app.root_path, 'utils', 'model_rekomendasi_rf.pkl')
    model_obj = None
    label_encoder = None
    if os.path.exists(xgb_path):
        artifact = joblib.load(xgb_path)
        if isinstance(artifact, dict) and 'model' in artifact:
            model_obj = artifact.get('model')
            label_encoder = artifact.get('label_encoder')
        else:
            model_obj = artifact
    elif os.path.exists(rf_path):
        model_obj = joblib.load(rf_path)
    else:
        flash("Model rekomendasi tidak ditemukan.")
        return redirect(url_for('siswa.dashboard_siswa'))

    paket_pred_raw = model_obj.predict([model_input])
    if label_encoder is not None:
        paket_label = label_encoder.inverse_transform(paket_pred_raw)[0]
    else:
        v = paket_pred_raw[0]
        s = str(v).strip()
        if s in {"Paket 1", "Paket 2", "Paket 3"}:
            paket_label = s
        elif s in {"0", "1", "2"}:
            i = int(s)
            paket_label = f"Paket {i+1}"
        else:
            paket_label = "Paket 1"

    paket_dict = {
        'Paket 1': ["Biologi", "Fisika", "Kimia", "Matematika"],
        'Paket 2': ["Biologi", "Matematika", "Ekonomi", "Sosiologi"],
        'Paket 3': ["Kimia", "Fisika", "Ekonomi", "Sosiologi"]
    }
    alasan_dict = {
        'Paket 1': "Paket 1 cocok berdasarkan hasil tes dan nilai rapor Anda.",
        'Paket 2': "Paket 2 cocok berdasarkan hasil tes dan nilai rapor Anda.",
        'Paket 3': "Paket 3 cocok berdasarkan hasil tes dan nilai rapor Anda."
    }
    semua_paket = paket_dict

    top3 = hasil_riasec.top3 if hasil_riasec else "-"
    paket = paket_label
    paket_mapel = paket_dict.get(paket_label, [])
    alasan = alasan_dict.get(paket_label, "Paket pilihan sesuai data Anda.")

    # --- SIMPAN REKOMENDASI KE DATABASE TANPA ALASAN ---
    if student:
        rekom = Recommendation.query.filter_by(id_student=student.id).first()
        if rekom:
            rekom.paket_prediksi = paket_label
            # rekom.timestamp = datetime.now() # jika punya kolom timestamp
        else:
            rekom = Recommendation(
                id_student=student.id,
                paket_prediksi=paket_label
                # timestamp=datetime.now() # jika punya kolom timestamp
            )
            db.session.add(rekom)
        db.session.commit()
    # --- END SIMPAN ---

    return render_template(
        'hasil_rekomendasi.html',
        top3=top3,
        paket=paket,
        paket_mapel=paket_mapel,
        alasan=alasan,
        semua_paket=semua_paket
    )
