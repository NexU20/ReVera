JGN DILIAT PLISS BUAT UAS DATA SCIENCE
# ReVera 🌟
**Shopee Sentiment Analysis Pipeline (End-to-End)**

ReVera adalah sebuah proyek *Data Science* end-to-end yang bertujuan untuk mengekstraksi, membersihkan, dan menganalisis sentimen dari ulasan pembeli di platform e-commerce Shopee. Proyek ini difokuskan pada analisis produk kosmetik dari toko **Forebie**, membagi ulasan ke dalam sentimen Positif, Netral, dan Negatif.

Proyek ini dibangun sebagai Tugas Akhir Mata Kuliah Sains Data pada Program Studi Teknik Informatika — FST UIN Syarif Hidayatullah Jakarta.

---

## ✨ Fitur Utama
1. **Robust Shopee Scraper**: Menggunakan *Playwright* dengan injeksi JavaScript untuk melakukan *bypass* terhadap *overlay-blocking* Shopee, memastikan proses ekstraksi ulasan yang mulus.
2. **Incremental Scraping**: Dukungan *mode append* (`--add`) untuk melanjutkan *scraping* data baru tanpa menimpa data yang sudah ada dan tanpa duplikasi.
3. **Advanced Text Preprocessing**: 
   - Menerjemahkan emoji menjadi makna teks menggunakan library `emoji` (contoh: 😭 -> `wajah_menangis_keras`).
   - Normalisasi kata, *case folding*, dan penghapusan *outliers* teks.
   - *Stopword Removal* dan *Stemming* cerdas menggunakan `Sastrawi`, sembari mempertahankan **kata-kata negasi** (tidak, bukan, jangan) agar konteks sentimen tetap akurat.
4. **Data Profiling & EDA**: Dilengkapi dengan Jupyter Notebook interaktif untuk visualisasi distribusi data, deteksi *outlier* via *boxplot*, dan pemetaan matriks korelasi (*heatmap*).
5. **Machine Learning Ready**: Menyajikan dataset akhir (*cleaned dataset*) yang terenkode dan siap dimasukkan ke dalam model klasifikasi.

---

## 📂 Struktur Direktori

```text
ReVera/
├── data/
│   ├── raw/                  # Dataset mentah hasil scraping (.csv)
│   └── processed/            # Dataset hasil feature engineering & cleaning
├── notebooks/
│   ├── 01_data_profiling_and_eda.ipynb   # Eksplorasi visualisasi data
│   └── 02_text_preprocessing.ipynb       # Tahapan pembersihan teks & Sastrawi
├── src/
│   ├── scraper/
│   │   └── scrape.py         # Script ekstraksi ulasan dari Shopee (Playwright)
│   └── preprocessing/
│       ├── feature_engineering.py   # Script penambahan fitur-fitur baru
│       └── text_preprocessing.py    # Script pembersihan teks & Stemming
├── doc/my-mine-kelompok/
│       ├── artikel_ilmiah_revera.md       # Artikel Ilmiah (Bahasa Indonesia)
│       ├── artikel_ilmiah_revera_en.md    # Artikel Ilmiah (Bahasa Inggris)
│       ├── presentasi_revera.html         # Slide Presentasi interaktif (HTML/CSS/JS)
│       ├── presentasi_revera.pdf          # Slide Presentasi versi PDF (Fullscreen)
│       ├── generate_pdf.py                # Script untuk men-generate PDF presentasi
│       └── detail-tugas.txt               # Rubrik dan kriteria penugasan kampus
├── env/                      # Python Virtual Environment
├── analyze_dataset.py        # Script profiling singkat lewat CLI
├── products.txt              # Daftar URL produk Shopee target scraping
└── README.md                 # Halaman utama ini
```

---

## 🚀 Cara Instalasi

1. Pastikan Python 3.9+ sudah terinstall.
2. Clone repository ini.
3. Aktifkan *virtual environment*:
   ```bash
   # Windows
   .\env\Scripts\activate
   ```
4. Install semua pustaka yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```
5. Install *browser binaries* untuk Playwright (jika belum):
   ```bash
   playwright install
   ```

---

## 💻 Panduan Penggunaan

### 1. Scraping Ulasan Shopee
Untuk mengambil data mentah dari daftar produk di `products.txt`:
```bash
# Mode timpa (overwrite)
python src/scraper/scrape.py

# Mode tambah (append data baru tanpa menimpa yang lama)
python src/scraper/scrape.py --add
```

### 2. Feature Engineering
Menambahkan fitur turunan (*Feature Engineering*) seperti `nama_produk`, `jumlah_kata`, dan label target:
```bash
python src/preprocessing/feature_engineering.py
```
*Hasil akan tersimpan di `data/processed/dataset_fitur.csv`*

### 3. Exploratory Data Analysis (EDA)
Gunakan Jupyter Notebook untuk melihat visualisasi dan pola data:
- Buka `notebooks/01_data_profiling_and_eda.ipynb` lalu jalankan (*Run All*).

### 4. Text Preprocessing (Cleansing & Stemming)
Membersihkan tanda baca, *demojize* emoji, membuang kata hubung, dan merubah ke kata dasar:
```bash
python src/preprocessing/text_preprocessing.py
```
*Hasil akan tersimpan di `data/processed/dataset_cleaned.csv` dan siap untuk tahap Pemodelan ML.*

### 5. Laporan & Presentasi
Seluruh dokumen hasil analisis akhir (Artikel Ilmiah dan Slide Presentasi) sudah disiapkan dan tersimpan di dalam folder `doc/my-mine-kelompok/`.
- **Slide Presentasi (Interaktif)**: Buka file `doc/my-mine-kelompok/presentasi_revera.html` menggunakan browser (sangat disarankan saat presentasi).
- **Slide Presentasi (PDF)**: Tersedia di `doc/my-mine-kelompok/presentasi_revera.pdf` sebagai backup/print.
- **Artikel Ilmiah**: Tersedia dalam dua bahasa, yaitu `doc/my-mine-kelompok/artikel_ilmiah_revera.md` (ID) dan `doc/my-mine-kelompok/artikel_ilmiah_revera_en.md` (EN).

---

## 🤝 Created by Me n The bois
- Me
- The bois:
    - *Goadex*
    - *Claude*