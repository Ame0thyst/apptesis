# Aplikasi Web Rekomendasi Paket Mata Pelajaran SMA (RIASEC + Nilai Rapor + ML)

## Tech Stack
- Flask (Python backend)
- MySQL (XAMPP)
- Tailwind CSS + Jinja2 (frontend)
- Model ML: Random Forest (.pkl)

## Langkah Jalankan

1. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
2. **Atur `.env` dan koneksi database di `config.py`**
3. **Jalankan migrasi database:**
    ```
    flask db init
    flask db migrate
    flask db upgrade
    ```
4. **Letakkan file model ML (`model_rekomendasi_rf.pkl`) di `app/utils/`**
5. **Jalankan aplikasi:**
    ```
    python run.py
    ```

## Catatan
- Password di database masih plaintext (untuk demo, ganti dengan hash di produksi).
- Semua template sudah pakai Tailwind via CDN.
- CRUD user, export/import, dsb. bisa kamu lengkapi sesuai kebutuhan.