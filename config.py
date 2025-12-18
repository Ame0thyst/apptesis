import os
from dotenv import load_dotenv

# Muat variabel dari file .env jika tersedia
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme123')
    # Gunakan DATABASE_URL dari .env jika ada, fallback ke default Laragon (root tanpa password)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root@localhost/db_rekomendasi')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
