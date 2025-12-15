import argparse
import os
import sys
import time
from collections import Counter
import pickle

# Set GUI backend sebelum import pyplot agar plt.show() dapat memunculkan window di desktop
import matplotlib
try:
    matplotlib.use("TkAgg")
except Exception:
    # jika TkAgg tidak tersedia, biarkan matplotlib memilih backend; plt.show() mungkin gagal kemudian
    pass
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import seaborn as sns
sns.set(style="whitegrid")

# XGBoost dan tools ML
try:
    import xgboost as xgb
except Exception:
    print("ERROR: xgboost belum terpasang di environment ini. Pasang xgboost lalu jalankan ulang.", file=sys.stderr)
    print("Contoh: python -m pip install xgboost", file=sys.stderr)
    sys.exit(1)

from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def parse_args():
    p = argparse.ArgumentParser(description="Train XGBoost with SMOTE, show popups, and save a single .pkl file.")
    p.add_argument(
        "--data",
        default=r"D:/2. S-2 UNY/TESIS/2. DATA DAN SISTEM/DATASET/DATASET RIASEC DAN NILAI RAPOR.csv",
        help="Path to input CSV dataset (default internal)."
    )
    p.add_argument(
        "--model-path",
        default="model_rekomendasi_xgb.pkl",
        help="Path lengkap untuk menyimpan .pkl (default: ./model_rekomendasi_xgb.pkl). Skrip TIDAK membuat folder baru."
    )
    p.add_argument("--test-size", type=float, default=0.2, help="Proporsi test set (default 0.2).")
    p.add_argument("--random-state", type=int, default=42, help="Random state untuk reproduktibilitas.")
    p.add_argument("--n-estimators", type=int, default=100, help="Jumlah boosting rounds/trees (default 100).")
    p.add_argument("--max-depth", type=int, default=5, help="Max depth trees (default 5).")
    p.add_argument("--learning-rate", type=float, default=0.1, help="Learning rate (eta) (default 0.1).")
    p.add_argument("--sampling-strategy", default="auto",
                   help="SMOTE sampling_strategy ('auto' atau 'to_max'). 'to_max' upsample semua kelas ke jumlah mayoritas.")
    # Default behavior: show popups (mirip skrip RandomForest Anda). Jika ingin non-interactive, jalankan dengan --no-show
    p.add_argument("--no-show", action="store_true", help="Jangan tampilkan popup figure (headless).")
    return p.parse_args()


def validate_model_path(model_path):
    """
    Pastikan direktori target untuk model ada. Jika model_path hanya filename (cwd) -> OK.
    Jika berisi direktori dan direktori tidak ada -> return False dan path direktori.
    """
    dirpath = os.path.dirname(os.path.abspath(model_path))
    if dirpath and not os.path.isdir(dirpath):
        return False, dirpath
    return True, dirpath


def plot_and_show_confusion(cm, classes, title="Confusion Matrix", show_popup=True):
    """
    Gambar confusion matrix (counts) dan tampilkan popup jika show_popup=True.
    Popup akan menunggu sampai Anda menutup jendela (plt.show(block=True)).
    """
    plt.figure(figsize=(6, 5))
    ax = sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                     xticklabels=classes, yticklabels=classes,
                     linewidths=0.8, linecolor='white', square=True,
                     annot_kws={"size": 12, "weight": "bold"})
    ax.set_xlabel("Prediksi")
    ax.set_ylabel("Aktual")
    ax.set_title(title)
    plt.tight_layout()
    if show_popup:
        try:
            plt.show(block=True)
        except Exception as e:
            print("Peringatan: plt.show() gagal (mungkin backend GUI tidak tersedia):", e, file=sys.stderr)
    plt.close()


def plot_and_show_feature_importance(importances, features, title="Feature Importance", show_popup=True):
    """
    Gambar feature importance dan tampilkan popup jika show_popup=True.
    """
    indices = np.argsort(importances)[::-1]
    plt.figure(figsize=(10, 6))
    plt.title(title)
    plt.bar(range(len(importances)), importances[indices], align='center', color='tab:blue')
    plt.xticks(range(len(importances)), [features[i] for i in indices], rotation=45, ha='right')
    plt.tight_layout()
    if show_popup:
        try:
            plt.show(block=True)
        except Exception as e:
            print("Peringatan: plt.show() gagal (mungkin backend GUI tidak tersedia):", e, file=sys.stderr)
    plt.close()


def main():
    args = parse_args()

    data_path = args.data
    model_path = args.model_path
    show_popup = not args.no_show

    # Fitur yang diharapkan pada dataset (sesuaikan jika beda)
    features = ['R', 'I', 'A', 'S', 'E', 'C',
                'BIOLOGI', 'FISIKA', 'KIMIA', 'MATEMATIKA', 'EKONOMI', 'SOSIOLOGI']
    paket_cols = ['Paket 1', 'Paket 2', 'Paket 3']

    # Validasi model_path: skrip tidak akan membuat folder baru
    ok, required_dir = validate_model_path(model_path)
    if not ok:
        print(f"ERROR: Direktori untuk menyimpan model tidak ditemukan: {required_dir}", file=sys.stderr)
        print("Skrip tidak akan membuat folder baru. Silakan buat folder tersebut terlebih dahulu atau gunakan --model-path tanpa direktori.", file=sys.stderr)
        sys.exit(1)

    # ----- load data -----
    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        print("Gagal membaca CSV:", e, file=sys.stderr)
        sys.exit(1)

    # ----- validasi kolom -----
    missing = [c for c in features + paket_cols if c not in df.columns]
    if missing:
        print("ERROR: Kolom tidak ditemukan di CSV:", missing, file=sys.stderr)
        print("Kolom tersedia:", df.columns.tolist(), file=sys.stderr)
        sys.exit(1)

    # ----- cek NaN -----
    if df[features].isnull().any().any():
        print("ERROR: Terdapat nilai NaN pada kolom fitur. Harap imputasi atau hapus baris yang memiliki NaN sebelum melanjutkan.", file=sys.stderr)
        sys.exit(1)
    if df[paket_cols].isnull().any().any():
        print("ERROR: Terdapat nilai NaN pada kolom paket. Harap periksa dataset.", file=sys.stderr)
        sys.exit(1)

    # ----- siapkan X dan y -----
    X = df[features].copy()
    y_raw = df[paket_cols].idxmax(axis=1)  # label string seperti 'Paket 1'

    # ----- LabelEncoder (fit pada seluruh dataset supaya mapping konsisten) -----
    le = LabelEncoder()
    le.fit(y_raw)
    classes = list(le.classes_)

    # ----- split data (stratify) -----
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_raw, test_size=args.test_size, random_state=args.random_state, stratify=y_raw
        )
    except Exception as e:
        print("Gagal melakukan train_test_split. Pesan:", e, file=sys.stderr)
        print("Kemungkinan beberapa kelas terlalu sedikit untuk stratify. Periksa distribusi kelas atau kurangi test-size.", file=sys.stderr)
        sys.exit(1)

    # ----- SMOTE pada training set -----
    paket_count = Counter(y_train)
    print("Distribusi sebelum SMOTE (train):", paket_count)

    if args.sampling_strategy == "to_max":
        max_count = max(paket_count.values())
        sampling_strategy = {label: max_count for label in paket_count}
    else:
        sampling_strategy = "auto"

    smote = SMOTE(random_state=args.random_state, sampling_strategy=sampling_strategy)
    try:
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    except Exception as e:
        print("SMOTE gagal:", e, file=sys.stderr)
        if args.sampling_strategy == "to_max":
            print("Mencoba fallback sampling_strategy='auto'...", file=sys.stderr)
            smote = SMOTE(random_state=args.random_state, sampling_strategy="auto")
            try:
                X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
            except Exception as e2:
                print("SMOTE fallback gagal:", e2, file=sys.stderr)
                sys.exit(1)
        else:
            sys.exit(1)

    print("Distribusi setelah SMOTE (train):", Counter(y_train_res))

    # ----- encode label numerik untuk training -----
    y_train_enc = le.transform(y_train_res)

    # ----- definisi model XGBoost -----
    xgb_clf = xgb.XGBClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.learning_rate,
        use_label_encoder=False,
        eval_metric='mlogloss',
        n_jobs=-1,
        random_state=args.random_state
    )

    # ----- training -----
    t0 = time.time()
    try:
        xgb_clf.fit(X_train_res, y_train_enc)
    except Exception as e:
        print("Training XGBoost gagal:", e, file=sys.stderr)
        sys.exit(1)
    t1 = time.time()

    # ----- predict & evaluate -----
    y_pred_enc = xgb_clf.predict(X_test)
    try:
        y_pred = le.inverse_transform(y_pred_enc)
    except Exception as e:
        print("Inverse transform pada prediksi gagal:", e, file=sys.stderr)
        sys.exit(1)

    cm = confusion_matrix(y_test, y_pred, labels=classes)
    print("=== Confusion Matrix ===")
    print(cm)
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, digits=4))
    print("\n=== Accuracy ===")
    print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')

    # ----- tampilkan popup seperti di script RandomForest Anda -----
    # Confusion matrix popup (menunggu sampai ditutup)
    plot_and_show_confusion(cm, classes, title="Confusion Matrix (XGBoost)", show_popup=show_popup)

    # Feature importance popup (menunggu sampai ditutup)
    try:
        importances = xgb_clf.feature_importances_
        plot_and_show_feature_importance(importances, features, title="Feature Importance (XGBoost)", show_popup=show_popup)
    except Exception as e:
        print("Gagal membuat feature importance:", e, file=sys.stderr)

    # ----- Simpan HANYA file .pkl (model + metadata) -----
    model_artifact = {"model": xgb_clf, "label_encoder": le, "features": features}
    try:
        with open(model_path, "wb") as fh:
            pickle.dump(model_artifact, fh, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Model XGBoost dan metadata berhasil disimpan sebagai: {os.path.abspath(model_path)}")
    except Exception as e:
        print("Gagal menyimpan model:", e, file=sys.stderr)
        sys.exit(1)

    print(f"Waktu training (s): {t1 - t0:.1f}")


if __name__ == "__main__":
    main()