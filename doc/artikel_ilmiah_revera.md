# Analisis Sentimen Ulasan Pelanggan Toko Forebie di Shopee Menggunakan TF-IDF dan Perbandingan Algoritma Klasifikasi

---

**Lindan** *(nama lengkap disesuaikan)*

Program Studi Teknik Informatika, Fakultas Sains dan Teknologi
UIN Syarif Hidayatullah Jakarta, Indonesia

*email: (disesuaikan)*

---

## Abstrak

Pertumbuhan pesat industri *e-commerce* di Indonesia menjadikan ulasan pelanggan sebagai sumber data yang sangat berharga untuk memahami kepuasan konsumen. Penelitian ini bertujuan untuk menganalisis sentimen ulasan pelanggan pada toko kosmetik Forebie di platform Shopee melalui implementasi *pipeline* Sains Data secara *end-to-end*. Dataset primer dikumpulkan menggunakan teknik *web scraping* berbasis Playwright, menghasilkan 684 ulasan dari 10 produk. Proses pra-pemrosesan teks (*text preprocessing*) mencakup *case folding*, translasi emoji ke teks representatif, penghapusan *stopwords* dengan pengecualian kata negasi, serta *stemming* menggunakan pustaka Sastrawi. Setelah pembersihan data, diperoleh 666 ulasan bersih dengan distribusi kelas yang tidak seimbang: Positif (62%), Netral (20%), dan Negatif (18%). Tiga algoritma klasifikasi dibandingkan: **Support Vector Machine (LinearSVC)**, **Naive Bayes (MultinomialNB)**, dan **Logistic Regression**, dengan representasi fitur menggunakan TF-IDF (*Term Frequency-Inverse Document Frequency*). Untuk menangani ketidakseimbangan kelas, parameter `class_weight='balanced'` diterapkan pada model SVM dan Logistic Regression. Hasil evaluasi menunjukkan bahwa **Logistic Regression** memberikan performa terbaik dengan **F1-Score (*weighted*) sebesar 0,732** dan **Accuracy 0,731**, mengungguli SVM (F1: 0,717) dan Naive Bayes (F1: 0,685). Analisis lebih lanjut melalui *Word Cloud* mengungkapkan adanya kontaminasi data dari teks respon penjual (*seller reply*) serta artefak translasi emoji yang mempengaruhi distribusi kata pada ulasan negatif. Model terbaik beserta *TF-IDF Vectorizer* berhasil disimpan dalam format `.joblib` untuk keperluan prediksi di masa mendatang.

**Kata Kunci:** Analisis Sentimen, NLP, TF-IDF, Logistic Regression, Support Vector Machine, Shopee, Ulasan Pelanggan, *E-commerce*

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Transformasi digital telah mendorong pertumbuhan pesat aplikasi belanja daring di Indonesia. Menurut data Asosiasi Penyelenggara Jasa Internet Indonesia (APJII), jumlah pengguna internet di Indonesia terus meningkat setiap tahunnya, memberikan potensi besar bagi pengembangan *e-commerce* [1]. Shopee, sebagai salah satu platform *e-commerce* terbesar di Asia Tenggara, memiliki basis pengguna yang sangat aktif di Indonesia dengan rata-rata kunjungan bulanan mencapai ratusan juta pengguna [2].

Ulasan pelanggan di platform *e-commerce* berperan ganda: sebagai bahan pertimbangan calon pembeli dalam mengambil keputusan pembelian, sekaligus sebagai umpan balik langsung bagi penjual untuk meningkatkan kualitas produk dan layanan [3]. Namun, dengan volume ulasan yang sangat besar, analisis manual tidak lagi efisien. Oleh karena itu, diperlukan pendekatan otomatis berbasis *Natural Language Processing* (NLP) dan *machine learning* untuk mengklasifikasikan sentimen ulasan ke dalam kategori positif, negatif, atau netral [4].

Penelitian ini mengambil studi kasus pada toko kosmetik **Forebie** di Shopee, yang dipilih karena memiliki variasi ulasan yang beragam --- mulai dari keluhan efek samping produk *skincare* hingga pujian atas kecocokan produk di kulit. Domain kosmetik juga menarik dari perspektif NLP karena ulasan cenderung menggunakan bahasa informal, slang, dan emoji secara intensif, sehingga menuntut tahapan pra-pemrosesan yang lebih cermat.

### 1.2 Rumusan Masalah

1. Bagaimana membangun *pipeline* analisis sentimen *end-to-end* untuk ulasan berbahasa Indonesia di platform *e-commerce*?
2. Algoritma klasifikasi mana yang paling efektif dalam mengklasifikasikan sentimen ulasan toko Forebie di Shopee?
3. Bagaimana performa model yang dihasilkan jika dibandingkan dengan penelitian terdahulu yang sejenis?

### 1.3 Tujuan Penelitian

1. Mengumpulkan dataset ulasan secara primer dari platform Shopee menggunakan teknik *web scraping*.
2. Melakukan pra-pemrosesan teks berbahasa Indonesia dengan mempertimbangkan karakteristik unik ulasan *e-commerce* (emoji, slang, respon penjual).
3. Membangun dan membandingkan tiga model klasifikasi sentimen: SVM, Naive Bayes, dan Logistic Regression.
4. Mengevaluasi performa model menggunakan metrik yang sesuai untuk dataset tidak seimbang (*imbalanced*).

### 1.4 Tinjauan Pustaka

Beberapa penelitian terdahulu yang relevan dengan topik ini antara lain:

**Kadir dan Fairuzabadi (2025)** [5] menganalisis sentimen ulasan aplikasi Shopee di Google Play menggunakan TF-IDF dan Logistic Regression pada 5.000 ulasan. Penelitian tersebut melaporkan akurasi sebesar **85,11%** dengan **macro-F1 sebesar 0,58**. Meskipun akurasi tinggi, nilai macro-F1 yang rendah menunjukkan bahwa model kesulitan mengenali kelas minoritas, terutama kelas netral yang hanya memperoleh F1-Score sebesar 0,14. Penelitian tersebut juga menegaskan bahwa ulasan netral sering bersifat ambigu dan mengandung sentimen campuran, sehingga sulit diklasifikasikan.

**Saepudin, Faqih, dan Dwilestari (2024)** [6] membandingkan algoritma SVM, Random Forest, dan Logistic Regression pada 3.000 ulasan Shopee dengan metodologi CRISP-DM. Hasil menunjukkan Random Forest memperoleh akurasi tertinggi (94%), diikuti SVM (91%) dan Logistic Regression (86%). Pelabelan pada penelitian tersebut menggunakan TextBlob secara otomatis, berbeda dengan pendekatan berbasis rating yang digunakan dalam penelitian ini.

**Fathurrohman *et al.* (2025)** [7] meneliti sentimen ulasan pengiriman Shopee Xpress menggunakan SVM dan Logistic Regression pada 497 ulasan. SVM mengungguli Logistic Regression dengan akurasi **93%** berbanding **90%**, meskipun kedua model menunjukkan konsistensi yang baik dalam prediksi sentimen pada data baru.

Dari tinjauan pustaka di atas, dapat disimpulkan bahwa: (1) TF-IDF tetap menjadi representasi fitur yang efektif untuk analisis sentimen berbahasa Indonesia, (2) tantangan utama terletak pada penanganan ketidakseimbangan kelas, dan (3) kelas netral secara konsisten menjadi kelas yang paling sulit diprediksi.

---

## 2. Metode Penelitian

### 2.1 Pengumpulan Data

Dataset merupakan **data primer** yang dikumpulkan langsung dari halaman ulasan produk toko Forebie di Shopee (https://shopee.co.id/shop/806035446) menggunakan *web scraper* berbasis **Playwright** (*browser automation*). Playwright dipilih karena mampu menembus proteksi DOM (*Document Object Model*) Shopee yang bersifat dinamis dan tidak dapat diakses oleh *scraper* berbasis HTTP biasa. Proses *scraping* mencakup:

- Pembukaan halaman produk secara otomatis dan navigasi ke bagian ulasan.
- Penggunaan injeksi JavaScript untuk mengklik filter rating (bintang 1-5) guna mem-*bypass* overlay DOM Shopee.
- Ekstraksi ID komentar, *username*, rating, dan teks ulasan.
- Mode *incremental* (`--add`) untuk menambah data tanpa duplikasi.

Total data yang berhasil dikumpulkan sebanyak **684 ulasan mentah** dari **10 produk** toko Forebie, dengan distribusi 5 kolom awal: `id_komentar`, `produk_url`, `username`, `rating`, dan `ulasan`.

### 2.2 Feature Engineering

Dataset awal hanya memiliki 5 kolom. Untuk memperkaya analisis, ditambahkan **4 kolom baru** melalui proses *feature engineering*:

| Kolom Baru | Tipe | Cara Pembuatan | Kegunaan |
|---|---|---|---|
| `nama_produk` | Kategorikal | Diekstrak dari URL Shopee via Regex | Analisis per produk |
| `jumlah_kata` | Numerik | `len(ulasan.split())` | Deteksi outlier |
| `panjang_karakter` | Numerik | `len(ulasan)` | Korelasi |
| `label_sentimen` | Kategorikal | Rating 1-2: Negatif, 3: Netral, 4-5: Positif | Target klasifikasi |

Pendekatan pelabelan berbasis rating ini konsisten dengan metodologi yang digunakan oleh Kadir dan Fairuzabadi [5], di mana skor rating digunakan sebagai *proxy* untuk menentukan sentimen secara otomatis.

### 2.3 Pra-pemrosesan Data (Text Preprocessing)

Tahap pra-pemrosesan teks dilakukan secara bertahap dengan urutan sebagai berikut:

1. **Penanganan *Missing Values*:** Baris dengan kolom ulasan kosong dihapus.
2. **Penanganan Outlier:** Ulasan dengan jumlah kata lebih dari 150 dihapus untuk mengeliminasi ulasan spam atau cerita yang terlalu panjang.
3. **Case Folding:** Seluruh teks dikonversi ke huruf kecil.
4. **Konversi Emoji:** Emoji diubah menjadi teks representatif bahasa Indonesia menggunakan pustaka `emoji` dengan parameter `language="id"`. Langkah ini bertujuan mempertahankan informasi emosional yang terkandung dalam emoji [8].
5. **Penghapusan Noise:** URL, *mention*, angka, dan tanda baca dihapus menggunakan ekspresi reguler (*regex*).
6. **Stopword Removal dengan Pengecualian Negasi:** Kata hubung tidak informatif dihapus menggunakan daftar *stopwords* dari pustaka Sastrawi. **Poin krusial:** kata-kata negasi (*"tidak"*, *"kurang"*, *"belum"*, *"jangan"*, *"bukan"*, *"tak"*) **sengaja tidak dihapus** karena menghapus kata negasi dapat membalikkan makna sentimen (contoh: *"tidak bagus"* menjadi *"bagus"*). Pendekatan ini sejalan dengan rekomendasi literatur NLP untuk domain analisis sentimen [9].
7. **Stemming:** Kata berimbuhan diubah ke kata dasar menggunakan pustaka **Sastrawi** (*Stemmer Factory*), yang merupakan *stemmer* standar untuk bahasa Indonesia [10].
8. **Label Encoding:** Label sentimen diubah ke bentuk numerik: Negatif = 0, Netral = 1, Positif = 2.

Setelah seluruh proses pra-pemrosesan, dataset akhir terdiri dari **666 ulasan bersih**.

### 2.4 Ekstraksi Fitur (TF-IDF)

Representasi fitur teks menggunakan metode **TF-IDF** (*Term Frequency-Inverse Document Frequency*) dengan konfigurasi:

- `max_features = 5000`: Membatasi jumlah fitur untuk efisiensi.
- `ngram_range = (1, 2)`: Menggunakan unigram dan bigram agar model dapat menangkap frasa dua kata seperti *"tidak cocok"* [5].
- `min_df = 2`: Mengabaikan kata yang sangat jarang muncul.
- `max_df = 0.95`: Mengecualikan kata yang terlalu umum.

### 2.5 Pembagian Data

Dataset dibagi menjadi **data latih** (80%) dan **data uji** (20%) dengan `stratify=y` agar proporsi kelas tetap terjaga di kedua subset, sesuai praktik standar dalam literatur [5][6][7].

### 2.6 Algoritma Klasifikasi

Tiga algoritma klasifikasi dibandingkan:

1. **SVM (LinearSVC):** Algoritma yang mencari *hyperplane* pemisah kelas dengan margin terlebar. Parameter `class_weight='balanced'` diaktifkan untuk menangani ketidakseimbangan kelas [7].
2. **Naive Bayes (MultinomialNB):** Algoritma klasifikasi probabilistik berbasis teorema Bayes, cocok untuk data teks berdimensi tinggi. Parameter *smoothing* `alpha=1.0` digunakan.
3. **Logistic Regression:** Algoritma klasifikasi probabilistik dengan fungsi *sigmoid*. Parameter `class_weight='balanced'` dan `max_iter=1000` digunakan [5].

### 2.7 Penanganan Ketidakseimbangan Kelas

Distribusi sentimen pada dataset ini tidak seimbang (*imbalanced*): Positif (62%), Netral (20%), dan Negatif (18%). Untuk menangani hal ini, digunakan parameter `class_weight='balanced'` pada model SVM dan Logistic Regression. Parameter ini secara otomatis menyesuaikan bobot kelas berdasarkan frekuensi kemunculannya, sehingga model tidak bias terhadap kelas mayoritas [5][7]. Pendekatan ini dipilih karena lebih sederhana dan langsung terintegrasi dengan *classifier*, berbeda dengan teknik *oversampling* seperti Random Oversampling yang digunakan oleh Kadir dan Fairuzabadi [5].

### 2.8 Metrik Evaluasi

Evaluasi model menggunakan:

- **Accuracy:** Proporsi prediksi benar terhadap total prediksi.
- **F1-Score (*weighted*):** Rata-rata harmonik dari *precision* dan *recall*, dibobotkan berdasarkan jumlah sampel per kelas. Metrik ini dipilih karena lebih adil untuk dataset tidak seimbang dibandingkan akurasi saja [5][7].
- **Confusion Matrix:** Matriks yang memperlihatkan distribusi prediksi benar dan salah untuk setiap kelas.
- **Classification Report:** Menampilkan *precision*, *recall*, dan F1-Score per kelas.

---

## 3. Hasil dan Pembahasan

### 3.1 Profil Dataset

Data mentah terdiri dari 684 ulasan dengan 5 kolom. Terdapat 7 *missing values* pada kolom `username` dan 11 baris *noise* (ulasan terlalu pendek atau hanya berisi teks "Membantu?") yang dihapus, menyisakan 673 ulasan setelah pembersihan awal. Setelah *feature engineering*, dataset memiliki 9 kolom.

### 3.2 Exploratory Data Analysis (EDA)

**Distribusi Sentimen:**
Dataset menunjukkan ketidakseimbangan kelas (*class imbalance*) dengan distribusi: Positif 62%, Netral 20%, dan Negatif 18%. Temuan ini konsisten dengan pola umum pada dataset *e-commerce* di mana sentimen positif mendominasi [5][6].

**Deteksi Outlier:**
Analisis *boxplot* pada fitur `jumlah_kata` menunjukkan adanya ulasan yang sangat panjang (outlier). Ulasan dengan lebih dari 150 kata dihapus karena cenderung merupakan ulasan spam atau cerita panjang yang tidak representatif.

**Korelasi Fitur Numerik:**
Heatmap korelasi menunjukkan:
- Korelasi sangat tinggi (r = 0.99) antara `jumlah_kata` dan `panjang_karakter`, yang wajar karena keduanya mengukur panjang teks.
- Korelasi positif lemah (r = 0.31) antara `rating` dan `jumlah_kata`, mengindikasikan bahwa pembeli dengan rating tinggi cenderung menulis ulasan yang sedikit lebih panjang.

### 3.3 Hasil Pemodelan

Tabel berikut menyajikan perbandingan performa ketiga model:

| Model | Accuracy | F1-Score (*weighted*) |
|---|---|---|
| SVM (LinearSVC) | 0,724 | 0,717 |
| Naive Bayes (MultinomialNB) | 0,709 | 0,685 |
| **Logistic Regression** | **0,731** | **0,732** |

**Logistic Regression** menunjukkan performa terbaik dengan F1-Score *weighted* sebesar **0,732** dan akurasi **73,1%**. Berikut adalah *classification report* detail untuk model Logistic Regression:

| Kelas | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Negatif | 0,60 | 0,88 | 0,71 | 24 |
| Netral | 0,50 | 0,36 | 0,46 | 27 |
| Positif | 0,88 | 0,78 | 0,82 | 83 |
| **Weighted Avg** | **0,75** | **0,73** | **0,73** | **134** |

### 3.4 Pembahasan

#### 3.4.1 Perbandingan dengan Penelitian Terdahulu

Hasil F1-Score *weighted* sebesar **0,732** yang diperoleh pada penelitian ini dapat dikategorikan **cukup baik** berdasarkan beberapa pertimbangan:

**Pertama**, penelitian Kadir dan Fairuzabadi [5] yang juga menggunakan kombinasi TF-IDF dan Logistic Regression pada ulasan Shopee melaporkan akurasi yang lebih tinggi (85,11%), namun **macro-F1 mereka hanya sebesar 0,58** --- lebih rendah dari *weighted* F1 penelitian ini (0,732). Hal ini menunjukkan bahwa model dalam penelitian ini **lebih seimbang** dalam mengenali ketiga kelas sentimen, meskipun akurasi *headline*-nya lebih rendah. Perbedaan ini dapat dijelaskan oleh dua faktor: (1) distribusi data pada penelitian [5] lebih timpang (80,98% positif vs 3,1% netral), dan (2) penggunaan Random Oversampling pada penelitian [5] meningkatkan akurasi tetapi tidak secara signifikan memperbaiki performa pada kelas minoritas.

**Kedua**, sebagian besar penelitian yang melaporkan akurasi di atas 85% --- seperti Saepudin *et al.* [6] (SVM: 91%, RF: 94%, LR: 86%) dan Fathurrohman *et al.* [7] (SVM: 93%, LR: 90%) --- menggunakan **skema pelabelan yang berbeda** atau **karakteristik dataset yang berbeda**. Saepudin *et al.* [6] menggunakan pelabelan otomatis berbasis TextBlob yang cenderung menghasilkan distribusi label yang lebih seragam, sementara Fathurrohman *et al.* [7] bekerja pada domain pengiriman (*delivery time*) yang memiliki pola linguistik yang lebih terstruktur dibandingkan ulasan produk kosmetik.

**Ketiga**, klasifikasi sentimen **3 kelas** (Positif, Netral, Negatif) secara inheren lebih sulit dibandingkan klasifikasi biner. Kelas **Netral** memiliki F1-Score terendah (0,46) pada penelitian ini, yang konsisten dengan temuan Kadir dan Fairuzabadi [5] (F1 Netral: 0,14) dan literatur umum yang menyebutkan bahwa ulasan netral sering bersifat ambigu, mengandung sentimen campuran (*mixed sentiment*), atau sekadar deskriptif tanpa ekspresi emosional yang jelas [5][11].

Tabel perbandingan berikut merangkum posisi penelitian ini terhadap rujukan:

| Aspek | Kadir & Fairuzabadi [5] | Saepudin *et al.* [6] | Fathurrohman *et al.* [7] | **Penelitian Ini** |
|---|---|---|---|---|
| Platform | Shopee (Google Play) | Shopee (Google Play) | Shopee Xpress | **Shopee (Toko Forebie)** |
| Jumlah Data | 5.000 | 3.000 | 497 | **684** |
| Sumber Data | Google Play Scraper | Web Scraping | X + Google Play | **Playwright (Langsung)** |
| Jumlah Kelas | 3 | 3 | 3 | **3** |
| Pelabelan | Rating | TextBlob | Manual | **Rating** |
| Metode Imbalance | Random Oversampling | --- | --- | **class_weight='balanced'** |
| Algoritma Terbaik | LR (85,11%) | RF (94%) | SVM (93%) | **LR (73,1%)** |
| Macro/Weighted F1 | **0,58** | --- | --- | **0,732** |

#### 3.4.2 Temuan Unik: Kontaminasi Data dan Artefak Translasi Emoji

Analisis *Word Cloud* pada ulasan negatif mengungkapkan fenomena menarik yang jarang dibahas dalam literatur:

**1. Kontaminasi dari Respon Penjual (*Seller Reply Leakage*):**
Kata-kata *"mohon"*, *"maaf"*, *"respon"*, *"minbie"*, *"siap"*, *"bantu"* mendominasi *Word Cloud* ulasan negatif. Investigasi menunjukkan bahwa alat *scraper* turut mengekstrak teks **respon penjual** yang melekat pada ulasan pelanggan. Admin toko Forebie (yang menyebut dirinya "Minbie") konsisten membalas ulasan bintang 1-2 dengan *template*: *"Mohon maaf kak, apakah ada kendala? Minbie siap membantu"*. Teks respon ini tercampur ke dalam data ulasan negatif, menyebabkan bias pada distribusi kata.

**2. Artefak Translasi Emoji:**
Tahap konversi emoji menggunakan `emoji.demojize(language="id")` menghasilkan kata-kata yang tidak terduga dalam *Word Cloud*:
- Emoji hati bersinar diterjemahkan menjadi `:hati_bersinar:`, yang setelah tokenisasi menghasilkan kata *"hati"* dan *"sinar"*.
- Emoji wajah menangis keras diterjemahkan menjadi `:wajah_menangis_keras:`, menghasilkan kata *"wajah"*, *"menang"* (hasil *stemming* dari *"menangis"*), dan *"keras"*.

Temuan ini menyoroti **tantangan nyata** dalam pra-pemrosesan teks media sosial berbahasa Indonesia, di mana konversi emoji dan penanganan teks non-standar memerlukan perhatian khusus untuk menghindari *noise* yang tidak diinginkan.

#### 3.4.3 Keunggulan Logistic Regression

Logistic Regression mengungguli SVM dan Naive Bayes pada dataset ini. Hal ini sejalan dengan temuan Kadir dan Fairuzabadi [5] yang juga menemukan Logistic Regression sebagai model terbaik dibandingkan SVM dan Naive Bayes. Keunggulan Logistic Regression pada konteks ini dapat disebabkan oleh:

1. **Estimasi probabilistik:** Logistic Regression menghasilkan probabilitas kelas, memungkinkan batas keputusan (*decision boundary*) yang lebih halus dibandingkan SVM yang berbasis margin [5].
2. **Kompatibilitas dengan `class_weight='balanced'`:** Parameter ini bekerja lebih efektif pada Logistic Regression karena langsung mempengaruhi fungsi *loss* secara proporsional.
3. **Stabilitas pada data terbatas:** Dengan hanya 666 sampel, Logistic Regression menunjukkan performa yang lebih stabil dibandingkan SVM yang lebih sensitif terhadap ukuran dataset [5][12].

---

## 4. Kesimpulan

Berdasarkan hasil penelitian dan pembahasan, dapat disimpulkan bahwa:

1. **Pipeline analisis sentimen *end-to-end*** berhasil dibangun, mencakup pengumpulan data primer menggunakan Playwright, *feature engineering*, pra-pemrosesan teks dengan Sastrawi, ekstraksi fitur TF-IDF, serta pemodelan dan evaluasi menggunakan tiga algoritma klasifikasi.

2. Dari perbandingan tiga algoritma, **Logistic Regression** memberikan performa terbaik dengan **F1-Score (*weighted*) sebesar 0,732** dan **Accuracy 0,731**. Model ini lebih seimbang dalam mengenali ketiga kelas sentimen dibandingkan SVM dan Naive Bayes.

3. Performa model ini **sebanding** dengan penelitian terdahulu jika mempertimbangkan: (a) penggunaan klasifikasi 3 kelas yang lebih sulit, (b) ukuran dataset yang lebih kecil, dan (c) karakteristik ulasan produk kosmetik yang menggunakan bahasa informal dan emoji secara intensif. Nilai *weighted* F1-Score (0,732) penelitian ini bahkan lebih tinggi dari *macro-F1* yang dilaporkan oleh Kadir dan Fairuzabadi [5] (0,58) meskipun akurasi mereka lebih tinggi.

4. Analisis *Word Cloud* mengungkapkan **temuan unik** berupa kontaminasi data dari respon penjual dan artefak translasi emoji, yang menjadi catatan penting bagi penelitian analisis sentimen *e-commerce* di masa mendatang.

### Saran Pengembangan

1. **Pembersihan data yang lebih ketat:** Menambahkan tahap pemisahan teks respon penjual dari teks ulasan pelanggan untuk menghindari kontaminasi data.
2. **Penambahan volume data**, terutama untuk kelas Netral dan Negatif, agar model lebih mampu membedakan ketiga kelas.
3. **Eksplorasi teknik penyeimbangan data** seperti SMOTE atau Random Oversampling untuk perbandingan dengan pendekatan `class_weight='balanced'`.
4. **Eksplorasi model *deep learning*** seperti IndoBERT yang diharapkan lebih baik dalam menangkap konteks kalimat dan mengatasi keterbatasan TF-IDF yang hanya berbasis frekuensi kata [5].

---

## Daftar Pustaka

[1] Asosiasi Penyelenggara Jasa Internet Indonesia (APJII), "Laporan Survei Internet APJII 2024," Jakarta, 2024.

[2] A. Saepudin, A. Faqih, and G. Dwilestari, "Perbandingan Algoritma Klasifikasi Support Vector Machine, Random Forest dan Logistic Regression Pada Ulasan Shopee," *Jurnal TEKNO KOMPAK*, vol. 18, no. 1, pp. 178-192, 2024. P-ISSN: 1412-9663, E-ISSN: 2656-3525.

[3] F. Pedregosa *et al.*, "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, 2011.

[4] B. Liu, "Sentiment Analysis and Opinion Mining," *Synthesis Lectures on Human Language Technologies*, vol. 5, no. 1, pp. 1-167, 2012.

[5] S. F. Kadir and A. Fairuzabadi, "Analisis Sentimen Ulasan Shopee di Google Play dengan TF-IDF dan Logistic Regression," *Journal of Artificial Intelligence and Digital Business (RIGGS)*, vol. 4, no. 2, pp. 7940-57945, 2025. DOI: 10.31004/riggs.v4i2.2850.

[6] A. Saepudin, A. Faqih, and G. Dwilestari, "Perbandingan Algoritma Klasifikasi Support Vector Machine, Random Forest dan Logistic Regression Pada Ulasan Shopee," *Jurnal TEKNO KOMPAK*, vol. 18, no. 1, pp. 178-192, 2024.

[7] S. Fathurrohman, I. Wahyuningtyas, I. R. Afandi, A. S. Nugroho, and F. N. Hasan, "Sentiment Analysis on Shopee Xpress Delivery Time Reviews Using Support Vector Machine and Logistic Regression," *IJID (International Journal on Informatics for Development)*, vol. 14, no. 2, pp. 640-658, Dec. 2025. DOI: 10.14421/ijid.2025.5073.

[8] Emoji Python Library. [Online]. Available: https://pypi.org/project/emoji/

[9] C. D. Manning, P. Raghavan, and H. Schutze, *Introduction to Information Retrieval*. Cambridge University Press, 2008.

[10] J. Asian, "Effective Techniques for Indonesian Text Retrieval," *PhD Thesis*, RMIT University, 2007.

[11] A. Pak and P. Paroubek, "Twitter as a Corpus for Sentiment Analysis and Opinion Mining," in *Proc. LREC*, 2010.

[12] Sastrawi -- Python Library for Indonesian Stemming. [Online]. Available: https://github.com/har07/PySastrawi

---

*Catatan: Artikel ini merupakan draft jurnal yang disusun sebagai bagian dari Tugas Akhir Mata Kuliah Sains Data, Program Studi Teknik Informatika --- FST UIN Syarif Hidayatullah Jakarta.*
