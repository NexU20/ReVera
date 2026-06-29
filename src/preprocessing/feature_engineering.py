import logging
import re
from pathlib import Path

import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path("data/raw/dataset_ulasan_mentah.csv")
PROCESSED_DATA_PATH = Path("data/processed/dataset_fitur.csv")


def clean_noise(df: pd.DataFrame) -> pd.DataFrame:
    """Membersihkan ulasan yang terlalu pendek atau hanya berisi 'Membantu?'"""
    logger.info(f"Jumlah data sebelum pembersihan: {len(df)}")

    # Hapus baris dengan ulasan kosong atau sangat pendek (<= 10 karakter)
    mask_short = df["ulasan"].astype(str).apply(len) <= 10
    
    # Hapus ulasan yang isinya hanya "Membantu?"
    mask_membantu = df["ulasan"].astype(str).str.strip() == "Membantu?"
    
    noise_mask = mask_short | mask_membantu
    df_clean = df[~noise_mask].copy()
    
    logger.info(f"Dihapus {noise_mask.sum()} baris noise.")
    logger.info(f"Jumlah data setelah pembersihan: {len(df_clean)}")
    
    return df_clean


def extract_product_name(url: str) -> str:
    """Mengekstrak nama produk dari URL Shopee."""
    try:
        # URL format: https://shopee.co.id/Nama-Produk-Panjang-i.shopid.itemid?extra...
        parts = url.split("/")
        if len(parts) > 3:
            # Mengambil bagian nama produk dan menghapus '-i.shopid.itemid...'
            raw_name = parts[3]
            # Menghapus '-i.angka.angka' di bagian akhir
            clean_name = re.sub(r"-i\.\d+\.\d+(\?.*)?$", "", raw_name)
            # Mengganti '-' dengan spasi
            return clean_name.replace("-", " ")
        return url
    except Exception:
        return "Unknown Product"


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Menambahkan fitur-fitur baru ke dataset."""
    df_feat = df.copy()

    # 1. nama_produk: Ekstraksi dari URL
    logger.info("Menambahkan kolom 'nama_produk'...")
    df_feat["nama_produk"] = df_feat["produk_url"].apply(extract_product_name)

    # 2. jumlah_kata: Menghitung jumlah kata dalam ulasan
    logger.info("Menambahkan kolom 'jumlah_kata'...")
    df_feat["jumlah_kata"] = df_feat["ulasan"].astype(str).apply(lambda x: len(x.split()))

    # 3. panjang_karakter: Menghitung panjang string karakter
    logger.info("Menambahkan kolom 'panjang_karakter'...")
    df_feat["panjang_karakter"] = df_feat["ulasan"].astype(str).apply(len)

    # 4. label_sentimen: Mapping dari rating
    logger.info("Menambahkan kolom 'label_sentimen'...")
    def map_sentiment(rating):
        if pd.isna(rating):
            return "Unknown"
        rating = int(rating)
        if rating <= 2:
            return "Negatif"
        elif rating == 3:
            return "Netral"
        else:
            return "Positif"

    df_feat["label_sentimen"] = df_feat["rating"].apply(map_sentiment)
    
    return df_feat


def run_feature_engineering():
    """Fungsi utama untuk menjalankan pipeline feature engineering."""
    if not RAW_DATA_PATH.exists():
        logger.error(f"File dataset tidak ditemukan: {RAW_DATA_PATH}")
        return

    logger.info("Mulai Feature Engineering...")
    
    # 1. Load Data
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        logger.info(f"Berhasil memuat dataset dengan {len(df)} baris.")
    except Exception as e:
        logger.error(f"Gagal memuat dataset: {e}")
        return

    # 2. Cleaning Noise
    df_clean = clean_noise(df)
    
    # 3. Feature Engineering
    df_features = add_features(df_clean)
    
    # 4. Simpan hasil
    try:
        PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        df_features.to_csv(PROCESSED_DATA_PATH, index=False, encoding="utf-8")
        logger.info(f"Dataset berhasil disimpan ke {PROCESSED_DATA_PATH}")
        
        # Tampilkan beberapa informasi profiling singkat
        logger.info("\n=== HASIL FEATURE ENGINEERING ===")
        logger.info(f"Kolom saat ini: {list(df_features.columns)}")
        logger.info("\nDistribusi Label Sentimen:")
        print(df_features["label_sentimen"].value_counts())
        logger.info("\nSampel Data (5 baris pertama):")
        print(df_features[["nama_produk", "jumlah_kata", "panjang_karakter", "label_sentimen"]].head())
        
    except Exception as e:
        logger.error(f"Gagal menyimpan dataset: {e}")


if __name__ == "__main__":
    run_feature_engineering()
