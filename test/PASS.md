# Handoff Document: Shopee Sentiment Analysis (Forebie Store)

Dokumen ini berisi riwayat lengkap (*handover*) pengembangan *Machine Learning Pipeline* untuk sentimen analisis ulasan Shopee. Dokumen ini disiapkan untuk dioperasikan oleh AI Agent selanjutnya agar langsung memahami konteks proyek, masalah yang sudah diselesaikan, serta apa langkah selanjutnya.

---

## 1. Konteks Proyek
Tujuan utama proyek ini adalah menyelesaikan Tugas Akhir Mata Kuliah Sains Data (Sesuai rubrik `doc/detail-tugas.txt`), yaitu membangun *Machine Learning Pipeline (End-to-End)* berbasis bahasa Python.

**Dataset**: Data Ulasan Shopee (Data Primer) dari Toko Kosmetik "Forebie".

---

## 2. Apa Saja yang Telah Dilakukan & Diselesaikan?

### A. Tahap 1: Data Collection & Scraping (`src/scraper/scrape.py`)
- **Permasalahan Utama**: Scraper Playwright sebelumnya gagal mengeklik filter rating (1 bintang, 2 bintang) karena terhalang oleh *overlay* DOM Shopee (`div.wAMdpk`). Playwright selalu me-return timeout karena pointer *intercepted*.
- **Penyelesaian**: Mengganti metode klik biasa menjadi eksekusi langsung lewat *JavaScript DOM* (`page.evaluate("el => el.click()")`). Ini sukses mem-bypass *overlay block*.
- **Fitur Baru (Incremental Scraping)**: AI mengimplementasikan mode `--add` menggunakan argumen CLI. Scraper kini akan meload *history* `id_komentar` dari CSV yang lama (`seen_review_ids`), sehingga saat dijalankan kembali, scraper hanya akan menambahkan ulasan baru tanpa duplikasi.
- **Hasil**: Berhasil mengumpulkan **686 ulasan mentah** ke dalam `data/raw/dataset_ulasan_mentah.csv`.

### B. Tahap 2: Feature Engineering (`src/preprocessing/feature_engineering.py`)
- **Permasalahan**: Syarat tugas meminta minimal **6 fitur/kolom**, namun dataset asli hanya memiliki 5 fitur.
- **Penyelesaian**: AI menambahkan 3 fitur baru (Total menjadi 9 kolom):
  1. `nama_produk`: Ekstraksi reguler dari URL Shopee.
  2. `jumlah_kata`: Menghitung panjang spasi dari ulasan.
  3. `panjang_karakter`: Menghitung jumlah karakter (untuk analisis korelasi).
  4. `label_sentimen`: Pemetaan rating ke target kelas (1-2 = Negatif, 3 = Netral, 4-5 = Positif).
- **Hasil**: Dataset disimpan ke `data/processed/dataset_fitur.csv` dengan total 673 baris efektif (setelah spam/noise dihapus).

### C. Tahap 3: Data Profiling & EDA (`notebooks/01_data_profiling_and_eda.ipynb`)
- Membangun Jupyter Notebook untuk EDA sesuai syarat tugas akhir.
- **Temuan (Insights)**:
  - Distribusi Sentimen Imbalanced: **Positif (61.7%)**, Netral (19.7%), Negatif (18.6%).
  - Ulasan sangat panjang menjadi *Outliers* (max 238 kata).
  - Ada korelasi positif lemah (0.31) antara tingginya rating dengan `jumlah_kata`, mengindikasikan ulasan bagus cenderung sedikit lebih panjang.

### D. Tahap 4: Text Preprocessing (`src/preprocessing/text_preprocessing.py` & `notebooks/02_text_preprocessing.ipynb`)
- **Cleansing**: Case folding, penghapusan karakter non-alfabet, dan penghapusan *outliers* (>150 kata).
- **Emoji Handling**: Mentranslasikan emoji menjadi teks menggunakan pustaka `emoji` (`demojize(language='id')`). Contoh: 😭 -> `wajah_menangis_keras`. Hal ini krusial untuk analisis sentimen e-commerce.
- **Stopword Removal Khusus**: Menggunakan pustaka `Sastrawi`, namun AI **mengecualikan kata negasi** (seperti *"tidak"*, *"kurang"*, *"belum"*, *"jangan"*) agar makna sentimen tidak berbalik.
- **Stemming**: Memotong imbuhan menjadi kata dasar (*Sastrawi*).
- **Encoding Target**: Merubah teks `label_sentimen` menjadi numerik (0, 1, 2) lewat `LabelEncoder`.
- **Hasil**: Berhasil menelurkan dataset bersih yang benar-benar siap latih ke `data/processed/dataset_cleaned.csv` (666 baris).

### E. Tahap 5: Pemodelan ML & Evaluasi (`src/modeling/train_model.py` & `notebooks/03_modeling_and_evaluation.ipynb`)
- **TF-IDF Vectorization**: Mengubah teks ulasan bersih menjadi vektor numerik menggunakan TF-IDF (unigram + bigram, max 5000 fitur).
- **Train/Test Split**: Rasio 80:20 dengan `stratify=y` agar proporsi kelas sama di kedua set.
- **3 Model dibandingkan** (semua menggunakan `class_weight='balanced'` kecuali Naive Bayes):

| Model | Accuracy | F1-Score (Weighted) |
|---|---|---|
| SVM (LinearSVC) | 0.7388 | 0.7268 |
| Naive Bayes | 0.7090 | 0.6496 |
| **Logistic Regression** | **0.7313** | **0.7316** ← TERBAIK |

- **Logistic Regression** terpilih sebagai model terbaik berdasarkan F1-Score (metrik yang lebih relevan dibanding Accuracy untuk data imbalanced).
- **Model Persistence**: Model terbaik dan TF-IDF Vectorizer disimpan ke `models/best_model.joblib` dan `models/tfidf_vectorizer.joblib`.
- **Evaluasi**: Confusion Matrix, Classification Report (Precision/Recall/F1 per kelas), dan visualisasi perbandingan antar-model sudah lengkap di notebook.

---

## 3. Apa yang Belum Diselesaikan (Tantangan Tersisa)?
1. **Class Imbalance**: Distribusi data kelas Positif sangat dominan (62%). Sudah ditangani menggunakan `class_weight='balanced'`, namun performa kelas Netral masih rendah (F1=0.46). Ini karena banyak ulasan Netral (rating 3) yang isinya mirip Positif atau Negatif.

---

## 4. Rencana Selanjutnya (Action Plan)

Semua tahap teknis pipeline (Scraping → Feature Engineering → EDA → Text Preprocessing → Modeling & Evaluasi) sudah **SELESAI**.

Yang tersisa adalah tahap **Pelaporan** sesuai `doc/detail-tugas.txt`:

1. **Konsolidasi Notebook Final**:
   - Gabungkan seluruh narasi ke dalam satu/beberapa Notebook `.ipynb` yang rapi dan siap cetak PDF.
   
2. **Artikel Ilmiah**:
   - Menyusun draft naskah jurnal sesuai template SINTA atau jurnal internal kampus (JTI UIN Jakarta).

3. **Presentasi**:
   - Menyiapkan slide presentasi 5-10 menit.

---

## 5. File-File Penting

| File | Fungsi |
|---|---|
| `data/raw/dataset_ulasan_mentah.csv` | Dataset mentah hasil scraping (684 baris) |
| `data/processed/dataset_fitur.csv` | Dataset + fitur tambahan (673 baris) |
| `data/processed/dataset_cleaned.csv` | Dataset bersih siap modeling (666 baris) |
| `models/best_model.joblib` | Model Logistic Regression terbaik |
| `models/tfidf_vectorizer.joblib` | TF-IDF Vectorizer yang sudah di-fit |
| `notebooks/01_data_profiling_and_eda.ipynb` | EDA & Visualisasi |
| `notebooks/02_text_preprocessing.ipynb` | Cleansing & Stemming |
| `notebooks/03_modeling_and_evaluation.ipynb` | Training & Evaluasi ML |

---
*End of Document. Pipeline status: ✅ Modeling SELESAI — Siap Pelaporan.*