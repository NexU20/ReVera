# Analisis Dataset: `dataset_ulasan_mentah.csv`

## Ringkasan Cepat

| Metrik | Nilai | Status |
|--------|-------|--------|
| Total review | **468** | ⚠️ Kurang untuk SVM |
| Kolom | 5 (`id_komentar`, `produk_url`, `username`, `rating`, `ulasan`) | ✅ Sesuai schema |
| Missing values | **0** | ✅ Lengkap |
| Duplicate `id_komentar` | **0** | ✅ Tidak ada duplikat |
| Produk unik | **5** | ⚠️ Terlalu sedikit variasi |
| Review tidak berguna (≤10 char) | **43 (9.2%)** | ❌ Perlu dibersihkan |

---

## 1. Distribusi Rating

```
Rating 1: ████████████████████ 50  (10.7%)
Rating 2: █████████████        34  ( 7.3%)
Rating 3: ████████████████████████████ 72  (15.4%)
Rating 4: ██████████████████████████████████████ 97  (20.7%)
Rating 5: ██████████████████████████████████████████████████████████████████████████████████████ 215 (45.9%)
```

### Mapping ke Sentimen

| Sentimen | Rating | Jumlah | Persentase |
|----------|--------|--------|------------|
| **Negative** | 1-2 | 84 | 17.9% |
| **Neutral** | 3 | 72 | 15.4% |
| **Positive** | 4-5 | 312 | **66.7%** |

> [!WARNING]
> **Dataset sangat tidak seimbang (imbalanced).** Kelas Positive mendominasi ~67%. Untuk SVM classifier, ini akan membuat model bias ke prediksi Positive dan performa pada kelas Negative akan buruk.
>
> Idealnya untuk classification 3-kelas, minimal ~150-200 review per kelas (total ~500-600). Untuk 2-kelas (Positive vs Negative), minimal ~200 per kelas.

---

## 2. Distribusi Per Produk

| Produk | Total | ⭐1 | ⭐2 | ⭐3 | ⭐4 | ⭐5 |
|--------|-------|-----|-----|-----|-----|-----|
| Samsung Galaxy A16 LTE 8/128GB | 118 | 24 | 22 | 24 | 24 | 24 |
| Samsung Galaxy A07 4/64GB (Light Violet) | 95 | 15 | 8 | 24 | 24 | 24 |
| Samsung Galaxy A07 6/128GB | 74 | 7 | 3 | 16 | 24 | 24 |
| Samsung 43" Crystal UHD TV | 61 | 4 | 1 | 8 | 24 | 24 |
| Samsung Galaxy A07 4/64GB (Black) | 120 | 0 | 0 | 0 | 1 | **119** |

> [!CAUTION]
> **Samsung Galaxy A07 4/64GB (Black)** hampir seluruhnya rating 5 (119 dari 120). Ini kemungkinan besar bug scraper — filter rating tidak berhasil diklik untuk produk ini, sehingga hanya mengambil review default yang bias positif. Produk ini sangat merusak keseimbangan dataset.

> [!IMPORTANT]
> Hanya **1 produk** (Samsung A16) yang berhasil di-scrape dengan distribusi yang cukup merata. Produk lainnya masih bias ke rating tinggi.

---

## 3. Masalah Kualitas Data

### 3a. Review "Membantu?" (28 review / 6.0%)

Shopee menampilkan teks `Membantu?` sebagai placeholder UI, bukan review asli. Ada **28 review** yang isinya hanya `Membantu?`. Ini **harus dibuang** karena tidak mengandung informasi sentimen maupun aspek.

### 3b. Review Sangat Pendek ≤10 karakter (43 review / 9.2%)

Selain `Membantu?`, ada review seperti:
- `1:01`, `0:20`, `0:06` → Ini durasi video, bukan teks ulasan
- `3`, `1` → Angka saja, tidak bermakna

Total review yang **benar-benar tidak berguna** untuk NLP: **~43 review (9.2%)**

### 3c. Review Efektif

Setelah membuang review tidak berguna:
- **Efektif: ~425 review** (masih kurang)
- Dari 425, distribusi sentimen tetap bias Positive

---

## 4. Kesesuaian dengan AGENT.md

### ✅ Yang Sudah Sesuai

| Requirement | Status |
|------------|--------|
| Schema kolom sesuai | ✅ |
| Data masuk ke `data/raw/` | ✅ |
| Ada `id_komentar` unik | ✅ |
| Teks ulasan dalam Bahasa Indonesia | ✅ |
| Variasi panjang ulasan cukup (mean 143 char) | ✅ |

### ❌ Yang Belum Sesuai

| Requirement | Masalah |
|------------|---------|
| Data cukup untuk SVM training | ❌ 468 terlalu sedikit, apalagi setelah cleaning |
| Distribusi seimbang per sentimen | ❌ Positive 67% vs Negative 18% |
| Gatekeeper perlu Negative & rating-3 yang cukup | ❌ Hanya 84 Negative + 72 Neutral = 156 review yang masuk aspect tagging |
| Aspect tagging butuh variasi aspek | ⚠️ Semua dari Samsung → aspek terbatas pada packaging, keaslian, kinerja |
| Dual-track preprocessing butuh teks bermakna | ❌ 43 review tidak bermakna |

---

## 5. Rekomendasi Aksi

### 🔴 Prioritas Tinggi

1. **Buang review noise** — Hapus 43 review yang ≤10 karakter atau isinya `Membantu?` / durasi video saat preprocessing
2. **Scrape ulang Samsung A07 4/64GB Black** — Produk ini gagal mengambil review seimbang, hasilnya 119 rating-5. Cek apakah filter rating berhasil diklik
3. **Tambah produk** — 5 produk terlalu sedikit. Target minimal **15-20 produk** dari kategori berbeda:
   - Produk dengan rating overall rendah (3.0-3.5)
   - Kategori rawan komplain: fashion, makanan, kosmetik
   - Bukan hanya Samsung

### 🟡 Prioritas Sedang

4. **Gabungkan dengan dataset Kaggle** — Sesuai rekomendasi di [PASS.md](file:///c:/Lindan/Cool/ds/uas/shopee-sentiment-analysis/PASS.md#L748), gabungkan data Shopee scraping dengan dataset Kaggle Bahasa Indonesia. Simpan di `data/external/` lalu merge di `data/processed/`
5. **Target total minimal 1000-1500 review** setelah cleaning, dengan distribusi:
   - Negative: ~300-400
   - Neutral: ~200-300
   - Positive: ~400-500

### 🟢 Opsional

6. **Oversampling** — Jika data Negative tetap kurang, gunakan SMOTE atau random oversampling di tahap training
7. **Tambah kolom metadata** — `source`, `scraped_at`, `rating_filter` untuk tracking asal data

---

## Kesimpulan

> [!IMPORTANT]
> **Dataset saat ini BELUM cukup** untuk menjalankan full pipeline (SVM training + aspect tagging) dengan performa yang baik. Masalah utamanya:
> 1. **Jumlah terlalu sedikit** (468, efektif ~425)
> 2. **Sangat tidak seimbang** (Positive 67%)
> 3. **1 produk gagal scrape seimbang** (A07 Black = 99% rating 5)
> 4. **Noise data** (43 review tidak bermakna)
>
> Langkah minimum yang harus dilakukan: scrape ulang produk yang gagal, tambah lebih banyak produk, dan gabungkan dengan dataset Kaggle.
