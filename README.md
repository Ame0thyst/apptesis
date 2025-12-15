# Aplikasi Web Rekomendasi Paket Mata Pelajaran SMA

![Hero](app/static/img/hero_illustration.png)

**Ringkas**

- Platform rekomendasi paket mata pelajaran berbasis Tes RIASEC + Nilai Rapor + Model ML
- Peran pengguna: `siswa`, `guru`, `admin`
- Teknologi: Flask, SQLAlchemy, Alembic, Tailwind, Chart.js, scikit-learn/XGBoost, MySQL

## Fitur Utama

- Tes RIASEC terstruktur dengan paginasi dan progress
- Visualisasi hasil RIASEC (bar + radar chart) dan penjelasan dimensi
- Input nilai rapor 6 mapel (Biologi, Fisika, Kimia, Matematika, Ekonomi, Sosiologi)
- Rekomendasi paket pelajaran dengan confidence dan distribusi probabilitas
- Dashboard guru/admin: ringkasan siswa dan distribusi paket

## Arsitektur

- `app/__init__.py`: Factory Flask, registrasi blueprint, integrasi login & migrasi
- `app/routes/`: Route untuk `auth`, `siswa`, `guru`, `admin`
- `app/models.py`: Skema database (User, Student, RiasecQuestion/Answer/Result, ReportScore, Recommendation)
- `app/templates/`: Template Jinja + Tailwind
- `app/utils/`: Utilitas ML (`rekomendasi.py` loader model, file model `.pkl`)
- `migrations/`: Alembic untuk migrasi skema

## Tech Stack

- Backend: `Flask`, `Flask-Login`, `Flask-SQLAlchemy`, `Flask-Migrate`
- Database: `MySQL` (driver `PyMySQL`), alternatif SQLite untuk pengembangan
- ML: `scikit-learn` (RandomForest), `XGBoost` (opsional), `joblib`
- Frontend: `Tailwind CSS` (CDN), `Chart.js` (CDN)

## Persiapan Lingkungan

- Python 3.11/3.12 dengan virtualenv direkomendasikan
- Install dependensi:
  - `pip install -r requirements.txt`
  - Jika menggunakan XGBoost: `pip install xgboost imbalanced-learn seaborn matplotlib`
- File model `.pkl` diletakkan di `app/utils/`:
  - RandomForest: `app/utils/model_rekomendasi_rf.pkl`
  - XGBoost (artefak dict): `app/utils/model_rekomendasi_xgb.pkl`

## Konfigurasi

- File `config.py` membaca environment dari `.env`
- Variabel penting:
  - `SECRET_KEY`: rahasia sesi Flask
  - `DATABASE_URL`: contoh `mysql+pymysql://root@localhost/db_rekomendasi`
- Buat `.env` di root proyek:
  - `SECRET_KEY=changeme123`
  - `DATABASE_URL=mysql+pymysql://root@localhost/db_rekomendasi`

## Database & Migrasi

- Inisialisasi dan migrasi skema:
  - `flask db init`
  - `flask db migrate -m "init"`
  - `flask db upgrade`
- Skema inti ada di `app/models.py`
- Contoh basis data tersedia: `instance/db_rekomendasi.sqlite3` dan dump SQL `instance/db_rekomendasi.sql`

## Menjalankan Aplikasi

- Jalankan server pengembangan:
  - `python run.py`
- Aplikasi akan berjalan di `http://127.0.0.1:5000/`
- Login awal: buat user melalui CLI/DB atau lengkapi route registrasi sesuai kebutuhan

## Alur Pengguna

- Siswa
  - Login, masuk `Dashboard`
  - Kerjakan `Tes RIASEC` hingga selesai untuk menghasilkan `RiasecResult`
  - Isi `Nilai Rapor` 6 mapel
  - Buka `Hasil Rekomendasi` untuk melihat paket, confidence, dan probabilitas
- Guru
  - Melihat daftar siswa, status tes, dan distribusi paket di `dashboard_guru`
- Admin
  - Ringkasan jumlah siswa/guru, distribusi rekomendasi, dan ekspor data sederhana

## Rekomendasi Paket (ML)

- Fitur input model (urutan baku): `R, I, A, S, E, C, BIOLOGI, FISIKA, KIMIA, MATEMATIKA, EKONOMI, SOSIOLOGI`
- Loader prioritas:
  - Jika `model_rekomendasi_xgb.pkl` ada, diprioritaskan
  - Fallback ke `model_rekomendasi_rf.pkl`
- Artefak XGB diharapkan berisi: `{"model": xgb_clf, "label_encoder": le, "features": [...]}`
- Output dipetakan ke label manusia: `Paket 1/2/3`
- Confidence & probabilitas ditampilkan ketika model mendukung `predict_proba`

## Pelatihan Model XGBoost (Opsional)

- Skrip contoh: `app/utils/model_rekomendasi_rf.py` (nama file tetap, isi melatih XGB)
- Minimal argumen:
  - `python app/utils/model_rekomendasi_rf.py --data <path_dataset.csv> --model-path app/utils/model_rekomendasi_xgb.pkl`
- Dataset kolom wajib:
  - Fitur: `R, I, A, S, E, C, BIOLOGI, FISIKA, KIMIA, MATEMATIKA, EKONOMI, SOSIOLOGI`
  - Label one-hot: `Paket 1, Paket 2, Paket 3`
- Skrip melakukan:
  - Validasi kolom, train/test split (stratify)
  - SMOTE untuk penyeimbangan kelas
  - Training XGBClassifier, evaluasi, simpan `.pkl`

## Aset

- Logo: `app/static/img/logo.png`
- Ilustrasi: `app/static/img/hero_illustration.png`
- Ikon: `app/static/img/icon_ai.png`, `app/static/img/icon_personal.png`, `app/static/img/icon_akurat.png`
- Referensi visual tambahan bisa ditautkan via URL CDN sesuai kebutuhan

## Keamanan & Catatan

- Password disimpan plaintext untuk demonstrasi (`app/routes/auth.py`). Gunakan hashing (`werkzeug.security`) di produksi.
- Pastikan `.pkl` tidak mengandung data sensitif.
- Jangan commit `.env` atau kredensial database ke repository publik.

## Troubleshooting

- Rekomendasi selalu `Paket 1`
  - Pastikan siswa sudah menyelesaikan Tes RIASEC dan mengisi nilai rapor
  - Periksa urutan fitur saat inferensi sesuai training
  - Evaluasi distribusi kelas pada dataset; gunakan SMOTE
- Chart tidak tampil
  - Pastikan CDN `Chart.js` dapat diakses
  - Cek `skor_list` terisi di `hasil_riasec` route

## Lisensi

- Proyek untuk kebutuhan akademik/demonstrasi. 
