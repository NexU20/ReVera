import logging
import re
from pathlib import Path

import emoji
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.preprocessing import LabelEncoder

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

INPUT_PATH = Path("data/processed/dataset_fitur.csv")
OUTPUT_PATH = Path("data/processed/dataset_cleaned.csv")


class TextPreprocessor:
    def __init__(self):
        logger.info("Inisialisasi Sastrawi Stemmer dan Stopword Remover...")
        # Stemmer
        stemmer_factory = StemmerFactory()
        self.stemmer = stemmer_factory.create_stemmer()

        # Stopword Remover
        stopword_factory = StopWordRemoverFactory()
        stopwords = stopword_factory.get_stop_words()

        # Kata negasi sangat penting untuk analisis sentimen, jangan dihapus!
        negasi = ["tidak", "kurang", "belum", "jangan", "bukan", "tak"]
        self.stopwords = [word for word in stopwords if word not in negasi]

    def convert_emoji(self, text: str) -> str:
        """Mengubah emoji menjadi representasi teks."""
        try:
            # Demojize dengan bahasa Indonesia (jika didukung) atau default bahasa Inggris
            # Format hasilnya biasanya: :wajah_tersenyum: atau :smiling_face:
            text = emoji.demojize(text, language="id")
            # Hilangkan karakter titik dua dan underscore dari hasil demojize
            text = text.replace(":", " ").replace("_", " ")
            return text
        except Exception:
            # Fallback jika terjadi error
            return text

    def clean_text(self, text: str) -> str:
        """Case folding dan penghapusan tanda baca/angka."""
        try:
            text = str(text).lower()  # Case folding
            text = self.convert_emoji(text)  # Konversi emoji dulu sebelum tanda baca dihapus
            
            # Hapus username (opsional, jika ada mention)
            text = re.sub(r'@[A-Za-z0-9_]+', '', text)
            # Hapus URL
            text = re.sub(r'http\S+|www\S+|https\S+', '', text)
            # Hapus karakter non-alfabet (angka, tanda baca)
            text = re.sub(r'[^a-z\s]', ' ', text)
            # Hapus spasi berlebih
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        except Exception:
            return ""

    def remove_stopwords_and_stem(self, text: str) -> str:
        """Menghapus stopwords dan melakukan stemming (kata berimbuhan -> kata dasar)."""
        try:
            # Hapus stopwords manual
            words = text.split()
            words_filtered = [w for w in words if w not in self.stopwords]
            text_filtered = " ".join(words_filtered)
            
            # Stemming dengan Sastrawi
            return self.stemmer.stem(text_filtered)
        except Exception:
            return text

    def preprocess(self, text: str) -> str:
        """Fungsi pembungkus untuk seluruh pipeline teks."""
        cleaned = self.clean_text(text)
        if not cleaned:
            return ""
        processed = self.remove_stopwords_and_stem(cleaned)
        return processed


def run_pipeline():
    if not INPUT_PATH.exists():
        logger.error(f"File tidak ditemukan: {INPUT_PATH}")
        return

    logger.info("Memulai tahap Preprocessing (Cleansing, Stopwords, Stemming)...")
    
    try:
        df = pd.read_csv(INPUT_PATH)
        logger.info(f"Dataset dimuat dengan {len(df)} baris.")
    except Exception as e:
        logger.error(f"Gagal memuat dataset: {e}")
        return

    # 1. Menangani Missing Values
    logger.info("Menangani Missing Values...")
    df.dropna(subset=["ulasan"], inplace=True)
    
    # 2. Menangani Outliers (Ulasan > 150 kata seringkali berisik / spam, kita batasi)
    # Dari EDA, 75% data di bawah 43 kata, max 238. 
    # Kita buang ulasan ekstrim > 150 kata (opsional, tapi disarankan).
    sebelum = len(df)
    df = df[df["jumlah_kata"] <= 150].copy()
    logger.info(f"Dibuang {sebelum - len(df)} baris ulasan terlalu panjang (Outliers).")

    # 3. Text Preprocessing (Sastrawi memakan waktu, kita pasang iterasi agar user tidak panik)
    logger.info("Memulai pemrosesan teks (ini akan memakan waktu 1-2 menit untuk stemming)...")
    preprocessor = TextPreprocessor()
    
    # Kita aplikasikan dengan progress (jika memakai tqdm lebih bagus, tapi pakai apply biasa cukup cepat untuk 600 baris)
    df["ulasan_bersih"] = df["ulasan"].apply(preprocessor.preprocess)
    
    # Hapus baris yang ulasannya menjadi kosong setelah dibersihkan
    kosong_sebelum = len(df)
    df = df[df["ulasan_bersih"].str.strip() != ""]
    logger.info(f"Dibuang {kosong_sebelum - len(df)} baris karena menjadi kosong setelah preprocessing.")

    # 4. Feature Encoding (Label Sentimen -> Numerik)
    logger.info("Melakukan Feature Encoding dengan LabelEncoder...")
    encoder = LabelEncoder()
    # Mengubah Negatif, Netral, Positif menjadi angka (0, 1, 2)
    # Agar urutannya sesuai bobot (Negatif=0, Netral=1, Positif=2), kita petakan manual untuk kepastian:
    mapping_sentimen = {"Negatif": 0, "Netral": 1, "Positif": 2}
    df["label_encoded"] = df["label_sentimen"].map(mapping_sentimen)
    
    # Simpan mapping class jika diperlukan nanti
    logger.info(f"Mapping Class: {mapping_sentimen}")

    # 5. Simpan Hasil
    try:
        df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
        logger.info(f"Dataset hasil preprocessing berhasil disimpan ke {OUTPUT_PATH}")
        logger.info(f"Total baris akhir: {len(df)}")
            
    except Exception as e:
        logger.error(f"Gagal menyimpan dataset akhir: {e}")


if __name__ == "__main__":
    run_pipeline()
