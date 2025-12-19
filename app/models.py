from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'siswa', 'admin', dst
    
    # Tambahan fields untuk role='siswa'
    nisn = db.Column(db.String(20), unique=True, nullable=True)
    nama = db.Column(db.String(150), nullable=True)
    kelas = db.Column(db.String(20), nullable=True)

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nisn = db.Column(db.String(20), nullable=True)   # <--- tambahkan ini
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(50), nullable=True)  # <--- tambahkan ini
    user = db.relationship("User", backref="student", uselist=False)

class RiasecQuestion(db.Model):
    __tablename__ = "riasec_questions"
    id = db.Column(db.Integer, primary_key=True)
    pertanyaan = db.Column(db.String(255), nullable=False)
    dimensi = db.Column(db.String(1), nullable=False)  # 'R', 'I', 'A', 'S', 'E', 'C'

class RiasecAnswer(db.Model):
    __tablename__ = "riasec_answers"
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    id_question = db.Column(db.Integer, db.ForeignKey('riasec_questions.id'), nullable=False)
    skor = db.Column(db.Integer, nullable=False)  # 1 untuk YA, 0 untuk TIDAK

    student = db.relationship("Student", backref="riasec_answers")
    question = db.relationship("RiasecQuestion", backref="riasec_answers")

class RiasecResult(db.Model):
    __tablename__ = "riasec_results"
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    skor_R = db.Column(db.Integer, default=0, nullable=False)
    skor_I = db.Column(db.Integer, default=0, nullable=False)
    skor_A = db.Column(db.Integer, default=0, nullable=False)
    skor_S = db.Column(db.Integer, default=0, nullable=False)
    skor_E = db.Column(db.Integer, default=0, nullable=False)
    skor_C = db.Column(db.Integer, default=0, nullable=False)
    top3 = db.Column(db.String(3), nullable=True)

    student = db.relationship("Student", backref="riasec_result")

class ReportScore(db.Model):
    __tablename__ = 'report_scores'
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id'))
    biologi = db.Column(db.Integer)
    fisika = db.Column(db.Integer)
    kimia = db.Column(db.Integer)
    matematika = db.Column(db.Integer)
    ekonomi = db.Column(db.Integer)
    sosiologi = db.Column(db.Integer)

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    paket_prediksi = db.Column(db.String(50), nullable=False)
    probabilitas = db.Column(db.Float, nullable=True)
    # Optional: waktu pembuatan (jika ingin tracking)
    # created_at = db.Column(db.DateTime, default=db.func.now())

    student = db.relationship("Student", backref="recommendations")