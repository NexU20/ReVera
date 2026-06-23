"""Test run: buka halaman Shopee dengan Playwright.

Tujuan tahap ini cuma satu: memastikan kita bisa membuka halaman Shopee
lewat browser otomatis tanpa langsung diblokir anti-bot. Belum mengambil
data apa pun — itu untuk tahap berikutnya.

Catatan teknis:
- Browser dijalankan *headed* (terlihat). Shopee gampang memblokir mode
  headless, jadi untuk test run kita biarkan jendelanya muncul.
- Pakai *persistent context* (folder .browser_data) supaya cookie & sesi
  login tersimpan antar-run. Kalau perlu login manual, cukup sekali.
- Ada jeda waktu acak biar pola aksesnya tidak terlalu kaku.

Cara pakai:
    python src/scraper/test_open_shopee.py
    python src/scraper/test_open_shopee.py "https://shopee.co.id/<url-produk>"
"""

from __future__ import annotations

import sys
import time

from playwright.sync_api import Error as PlaywrightError, sync_playwright

from config import HOME_URL, PROFILE_DIR, ambil_halaman_aktif, buka_browser, jeda
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def main() -> int:
    """Open Shopee in a persistent browser context for a smoke test.

    Returns:
        Process exit code.
    """
    url = sys.argv[1] if len(sys.argv) > 1 else HOME_URL

    logger.info("Membuka: %s", url)
    logger.info("Profil browser: %s", PROFILE_DIR)

    with sync_playwright() as p:
        context = buka_browser(p)
        page = ambil_halaman_aktif(context)

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            jeda()

            judul = page.title()
            logger.info("Judul halaman: %r", judul)
            logger.info("URL sekarang: %s", page.url)

            # Deteksi halaman anti-bot: andalkan judul, bukan isi badan.
            # Kata seperti "verifikasi" sering muncul wajar di teks halaman,
            # jadi cek isi badan terlalu sering memberi alarm palsu.
            judul_lower = judul.lower()
            penanda_blokir = ("captcha", "verify", "access denied", "are you a human")
            if not judul or any(kata in judul_lower for kata in penanda_blokir):
                logger.warning("Judul halaman tidak normal, mungkin kena anti-bot")
            else:
                logger.info("Halaman tampak termuat normal")

            logger.info(
                "Jendela browser dibiarkan terbuka. Periksa halaman, lalu tekan Enter "
                "di terminal untuk menutup"
            )
            try:
                # Tunggu Enter kalau dijalankan interaktif. Kalau stdin tidak
                # tersedia (mis. dipanggil dari skrip), input() melempar EOF —
                # kita tangkap dan tutup otomatis setelah jeda.
                input()
            except EOFError:
                detik = 20
                logger.info("Tidak ada input interaktif; menutup otomatis dalam %s detik", detik)
                time.sleep(detik)
        except PlaywrightError as exc:
            logger.exception("Gagal membuka Shopee: %s", exc)
            return 1
        finally:
            context.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
