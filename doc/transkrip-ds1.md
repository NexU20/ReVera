# Transkrip Presentasi — Analisis Sentimen & Penandaan Aspek Ulasan Shopee

> **Cara pakai:** baca per slide. Kalimat di bawah ditulis seperti gaya ngomong, jadi bisa langsung dibaca. Bagian _(miring dalam kurung)_ adalah catatan untuk kamu sendiri — **jangan dibacakan**. Estimasi total: **8–11 menit**.

---

## Slide 1 — Judul

> _(Buka dengan tenang, senyum, lihat audiens dulu sebentar.)_

"Assalamualaikum warahmatullahi wabarakatuh. Selamat pagi/siang Bapak/Ibu dan teman-teman. Perkenalkan, kami dari kelompok [sebutkan nama kelompok / anggota].

Hari ini kami akan mempresentasikan rencana tugas akhir kami yang berjudul **'Analisis Sentimen dan Penandaan Aspek pada Ulasan Produk Shopee'**.

Singkatnya, tujuan kami adalah mengubah ulasan-ulasan teks yang berantakan di Shopee menjadi informasi keluhan yang rapi dan benar-benar bisa ditindaklanjuti oleh pemilik toko. Studi kasus kami fokus pada satu toko dengan lima produk terlarisnya."

---

## Slide 2 — Latar Belakang

"Jadi, kenapa kami mengambil topik ini?

Setiap hari ada jutaan transaksi di Shopee, dan itu menghasilkan ulasan dalam jumlah yang sangat banyak. Ulasan ini sebenarnya adalah **suara konsumen secara langsung** — sangat berharga buat penjual.

Masalahnya, **rating bintang saja tidak cukup**. Misalnya ada yang kasih bintang 4, kita tidak tahu *apa* sebenarnya yang bikin dia puas, atau bagian mana yang masih kurang. Informasi yang paling berharga itu justru ada di dalam **teksnya**, bukan di angka bintangnya.

Nah, untuk membacanya satu per satu secara manual itu mustahil karena jumlahnya terlalu banyak. Dan tantangan tambahannya: bahasa ulasan Shopee itu sangat informal. Penuh singkatan, kata tidak baku, huruf yang dipanjang-panjangin seperti 'mantulll', emoji, bahkan campur bahasa Indonesia dan Inggris.

Makanya solusi kami adalah menggabungkan dua hal: **analisis sentimen** untuk tahu ulasan itu positif, negatif, atau netral; dan **penandaan aspek** untuk tahu keluhannya soal apa. Dengan begitu, teks yang tadinya berantakan bisa berubah jadi data yang terstruktur."

---

## Slide 3 — Rumusan Masalah & Tujuan

"Dari latar belakang tadi, kami menyusun tiga pertanyaan penelitian.

**Pertama**, tahapan pra-pemrosesan seperti apa yang cocok untuk bahasa informal Shopee tadi, supaya teksnya bersih dan siap dianalisis.

**Kedua**, seberapa baik model kami — yaitu SVM dengan fitur TF-IDF — dalam mengklasifikasikan sentimen ke dalam tiga kelas: positif, negatif, dan netral.

**Ketiga**, aspek apa saja yang paling sering dikeluhkan konsumen, khususnya pada ulasan yang negatif dan bintang 3, dilihat dari sisi kualitas barang, kemasan, dan pengiriman.

Jadi tujuan akhirnya bukan cuma bilang 'rating turun', tapi memberi **rekomendasi yang tepat sasaran** ke pemilik toko: bagian mana persisnya yang harus diperbaiki."

---

## Slide 4 — Rencana Pengumpulan Data

"Untuk datanya, kami pakai **dua sumber yang saling melengkapi**.

**Sumber pertama** adalah objek utama kami: ulasan asli dari lima produk terlaris di toko target. Ini kami ambil langsung lewat teknik *web scraping* menggunakan pustaka **Playwright**. Kenapa Playwright? Karena halaman Shopee itu dimuat secara dinamis pakai JavaScript dan tidak menyediakan API publik. Kami juga pakai jeda waktu acak supaya pola aksesnya mirip manusia dan tidak membebani server.

**Sumber kedua** adalah dataset publik dari Kaggle, sebagai pemerkaya data latih. Ini penting karena produk terlaris biasanya didominasi ulasan positif, jadi contoh kelas negatif dan netral itu langka. Dataset publik ini kami pilih dari kategori sejenis untuk menambah contoh kelas yang langka tadi.

Dari sisi etika, kami mengikuti ketentuan layanan: ambil data seperlunya, hanya konten ulasan dan rating, mengabaikan data pribadi pengguna, dan murni untuk keperluan akademik.

_(Tegaskan bagian ini — biasanya ditanya dosen)_ Dan kami juga sudah siapkan **rencana cadangan**: kalau scraping-nya diblokir oleh sistem anti-bot Shopee, dataset publik bisa jadi tumpuan utama supaya proyek tetap jalan."

---

"Terima kasih. Singkatnya, proyek kami ini tentang analisis ulasan produk di Shopee.

Jadi masalahnya begini: di Shopee itu ulasannya banyak sekali, tapi rating bintang saja tidak menjelaskan apa-apa. Bintang 4 itu tidak memberi tahu kita kenapa pembeli puas atau kecewa. Yang berharga justru ada di teks ulasannya — cuma teksnya berantakan, penuh singkatan, typo, dan emoji, jadi tidak mungkin dibaca manual satu per satu.

Nah, yang kami bangun itu sebuah sistem yang melakukan dua hal. Pertama, analisis sentimen — mengelompokkan ulasan jadi positif, negatif, atau netral pakai model SVM. Kedua, penandaan aspek — khusus untuk ulasan yang negatif dan bintang 3, kami cari tahu keluhannya soal apa: apakah soal kualitas barang, kemasan, atau pengiriman. Tujuannya supaya pemilik toko tahu persis bagian mana yang harus diperbaiki.

Soal datanya dari mana, kami pakai dua sumber:

Yang pertama dan utama, ulasan asli dari 5 produk terlaris di satu toko target. Ini kami ambil langsung dari Shopee lewat teknik web scraping — kami pakai Playwright, karena halaman Shopee itu dimuat dinamis dan tidak punya API publik.

Yang kedua, dataset publik dari Kaggle sebagai data tambahan untuk melatih model. Ini kami butuhkan karena produk terlaris biasanya ulasannya positif semua, jadi contoh ulasan negatif dan netralnya sedikit. Dataset publik ini menambah contoh kelas yang langka tadi, supaya modelnya tidak berat sebelah.

Jadi intinya: ulasan asli toko sebagai objek analisis, dataset publik sebagai penyeimbang data latih."

---
Itu versi ringkas sekitar 1 menit. Mau saya bikinkan yang lebih pendek lagi (30 detik, buat jawab kalau dosen tanya "coba jelaskan sekilas projeknya"), atau yang ini sudah pas?

## Slide 5 — Pipeline Sistem (Dua Fase)

> _(Ini slide paling teknis. Pelan-pelan, tunjuk ke diagramnya.)_

"Ini adalah keseluruhan alur sistem kami. Yang perlu digarisbawahi: arsitekturnya terbagi jadi **dua fase**.

**Fase A — Membangun Model.** Di sini kami menggabungkan dataset publik dan sampel toko target yang sudah dilabeli, lalu masuk ke *preprocessing* berat, dibagi jadi data latih dan data uji secara *stratified*, kemudian diubah jadi fitur TF-IDF dan dipakai untuk melatih SVM. Hasil akhir fase ini adalah satu **model SVM terlatih** — kami sebut ini artefak. Di fase ini juga modelnya langsung dievaluasi pakai F1 makro dan confusion matrix.

**Fase B — Penerapan dan Analisis.** Nah, model dari Fase A tadi sekarang dipakai untuk data baru, yaitu ulasan toko target yang belum pernah dilatih. Di sini ulasannya dipecah ke **dua jalur preprocessing secara paralel**:

- **Jalur berat** untuk klasifikasi — hasilnya masuk ke model SVM tadi untuk diprediksi sentimennya, lalu disaring, diambil yang **negatif dan bintang 3**.
- **Jalur ringan** yang menjaga kata tetap utuh, untuk keperluan penandaan aspek.

Kedua jalur ini akhirnya **bertemu** di tahap **Regex aspect tagging**, yang mengelompokkan keluhan ke aspek kualitas, kemasan, dan pengiriman. Output akhirnya berupa distribusi keluhan dan wordcloud."

---

## Slide 6 — Rencana Pra-pemrosesan

"Sekarang kita masuk lebih detail ke pra-pemrosesan.

Awalnya, semua teks melewati **pembersihan dasar yang sama**: huruf dikecilkan, huruf berulang ditangani, emoji diubah jadi teks, kata slang dinormalisasi pakai kamus, dan ada pemetaan dwibahasa.

Setelah itu, teksnya dialirkan ke **dua jalur** — dan ini bagian yang kami anggap penting.

- **Jalur berat**, untuk SVM: ada tokenisasi, penghapusan stopword, dan stemming pakai Sastrawi. Tujuannya memadatkan jumlah fitur supaya modelnya fokus ke kata yang bermakna.
- **Jalur ringan**, untuk Regex: di sini kami sengaja **tidak pakai stemming** dan stopword agresif. Kenapa? Karena kalau katanya dipotong-potong, kata kunci keluhannya bisa rusak dan malah tidak terdeteksi.

Untuk pelabelan, kami pakai pendekatan **hibrida**: dilabeli otomatis dari rating, tapi khusus **ulasan bintang 3 kami verifikasi manual**, karena bintang 3 itu paling ambigu — sering campuran antara pujian dan keluhan. Kami juga punya aturan baku untuk kasus tepi, seperti ulasan satu kata atau yang isinya cuma emoji.

Dan untuk mengatasi data yang tidak seimbang tadi, contoh kelas minoritas kami tambah dari dataset publik."

---

## Slide 7 — Rencana Pemodelan

"Untuk pemodelannya.

Fiturnya pakai **TF-IDF dengan unigram dan bigram**. Bigram itu penting supaya frasa seperti 'tidak bagus' bisa tertangkap utuh — jangan sampai 'tidak' dan 'bagus' dibaca terpisah, karena maknanya bisa kebalik.

Algoritmanya pakai **Support Vector Machine**. Kami pilih SVM karena dia andal untuk data teks yang dimensinya tinggi, dan jauh lebih ringan dibanding deep learning — cocok untuk skala tugas kami.

Lalu ada bagian yang kami sebut **Gatekeeper**, atau gerbang penyaring. Jadi SVM jalan dulu, setelah itu sistem hanya meneruskan ulasan yang **negatif** dan yang **bintang 3** ke tahap analisis aspek. Ulasan positif dibuang supaya prosesnya efisien.

_(Tekankan ini — ini nilai jualnya)_ Kenapa gerbang ini penting? Karena dia bisa menangkap **anomali**: misalnya ada ulasan bintang tinggi tapi isinya ternyata keluhan. Dengan gerbang ini, keluhan tetap tertangkap walaupun ratingnya bagus.

Terakhir, untuk pembagian data kami pakai *stratified split* yang diperkuat *cross-validation*, dan sebagian data toko yang sudah dilabeli kami suntikkan ke data latih supaya model lebih menyesuaikan dengan gaya bahasa toko target."

---

## Slide 8 — Rencana Evaluasi

"Untuk evaluasi, kami pisahkan jadi dua, karena komponennya beda.

**Pertama, evaluasi sentimen** dari SVM — ini kuantitatif. Kami pakai Precision, Recall, dan F1 yang dilaporkan per kelas, lalu disimpulkan pakai **Macro-Average F1**. Kami sengaja pakai macro supaya kelas minoritas seperti negatif dan netral dapat bobot yang setara.

_(Poin penting)_ Dan kami **sengaja menghindari accuracy**. Kenapa? Karena kalau datanya didominasi positif, akurasi bisa kelihatan tinggi padahal modelnya gagal mengenali keluhan. Itu menyesatkan. Kami juga pakai confusion matrix untuk melihat pola kesalahannya, terutama di kelas netral dan bintang 3.

**Kedua, evaluasi aspek** dari Regex — ini kualitatif. Kami periksa manual pada sampel ulasan, untuk menguji apakah polanya menandai aspek dengan tepat dan apakah ada keluhan yang terlewat.

_(Jujur — justru ini yang dihargai penguji)_ Dan kami sadar betul keterbatasannya: **kelas netral kemungkinan akan jadi sumber error terbesar**, dan Regex juga punya batas pada variasi kata. Ini akan kami sampaikan secara terbuka di laporan, bukan kami sembunyikan."

---

## Slide 9 — Tools & Teknologi

> _(Slide ini cepat saja, tidak perlu disebut satu-satu.)_

"Untuk perkakasnya, seluruh pipeline kami bangun di atas **Python** supaya konsisten.

Garis besarnya: **Playwright dan pandas** untuk akuisisi dan pengolahan data; **Sastrawi, pustaka emoji, kamus slang, dan leksikon InSet** untuk pra-pemrosesan; lalu **scikit-learn** sebagai inti pemodelan — mulai dari TF-IDF, SVM, sampai perhitungan metriknya.

Untuk visualisasi kami pakai matplotlib, seaborn, dan wordcloud. Dan sebagai opsi tambahan, kami siapkan **Streamlit** untuk dashboard hasil yang interaktif."

---

## Slide 10 — Timeline & Milestone

"Ini rencana kerja kami, kurang lebih **delapan minggu**.

Dua minggu pertama untuk pengumpulan data — scraping sekaligus menyiapkan dataset publik. Lanjut ke pra-pemrosesan, lalu pelabelan dan verifikasi manual. Pertengahan jalan, kami fokus ke TF-IDF dan pelatihan SVM, dilanjutkan gerbang penyaring dan penandaan aspek. Setelah itu evaluasi dan tuning, dan minggu terakhir untuk visualisasi, penyusunan laporan, serta persiapan presentasi.

Milestone utamanya: minggu ke-2 data sudah terkumpul, minggu ke-4 dataset terlabel siap, minggu ke-6 model dan aspek sudah berjalan, dan minggu ke-8 laporan beserta demo selesai."

> _(Kalau timeline ini hanya ancang-ancang, bilang jujur: "Timeline ini masih bisa kami sesuaikan dengan kondisi di lapangan.")_

---

## Slide 11 — Risiko & Mitigasi

"Kami juga sudah memetakan risiko utama beserta cara mengatasinya.

**Satu**, risiko scraping diblokir anti-bot atau kendala ketentuan layanan. Kami mitigasi dengan jeda waktu acak, batasi volume, dan menyiapkan dataset publik sebagai cadangan.

**Dua**, risiko data tidak seimbang dan ambiguitas bintang 3. Kami atasi dengan menyuntikkan data kelas minoritas dan pelabelan hibrida yang pakai aturan baku.

**Tiga**, risiko *domain mismatch* dan performa kelas netral yang menurun. Ini kami tangani dengan menggabungkan kosakata dari dua sumber data, dan kelemahannya kami petakan lewat confusion matrix.

**Empat**, risiko Regex gagal menangkap variasi kata. Mitigasinya, polanya kami rancang untuk mencocokkan teks yang sudah dinormalisasi, dan kami uji manual pada sampel."

---

## Slide 12 — Penutup

> _(Pelan, tutup dengan percaya diri.)_

"Jadi sebagai penutup: lewat proyek ini kami ingin mengubah ulasan yang berantakan menjadi keluhan yang benar-benar bisa ditindaklanjuti — dari pengumpulan data, pembersihan, pelabelan, klasifikasi SVM, gerbang penyaring, penandaan aspek, sampai evaluasi.

Tiga hal yang kami jaga sepanjang proyek ini adalah **transparansi**, kesadaran akan **keterbatasan**, dan adanya **rencana cadangan**.

Sekian presentasi dari kelompok kami. Terima kasih atas perhatiannya, dan kami persilakan kalau ada pertanyaan atau masukan. Wassalamualaikum warahmatullahi wabarakatuh."

---

## Lampiran — Antisipasi Pertanyaan Penguji

> _(Tidak dibacakan. Siapkan jawaban singkat untuk ini.)_

- **"Kenapa SVM, bukan deep learning / IndoBERT?"** → Karena skala data dan sumber daya kami terbatas; SVM andal untuk teks dimensi tinggi, ringan, dan hasilnya mudah dijelaskan. Deep learning bisa jadi pengembangan lanjutan.
- **"Kalau scraping gagal total, proyek tetap jalan?"** → Iya, dataset publik jadi tumpuan utama. Kami sudah tetapkan jumlah minimal ulasan.
- **"Regex itu kan kaku, bagaimana kalau banyak typo?"** → Betul, itu keterbatasan yang kami akui. Polanya dijalankan setelah normalisasi slang, dan diuji manual. Pengembangan ke depan bisa pakai pendekatan berbasis embedding.
- **"Bagaimana memastikan label bintang 3 tidak subjektif?"** → Pakai aturan baku dan verifikasi manual; idealnya dicek oleh lebih dari satu orang untuk konsistensi.
- **"Kenapa menghindari accuracy?"** → Karena data didominasi positif, accuracy bisa tinggi palsu. Macro-F1 lebih adil untuk kelas minoritas.
