"""Login Shopee sekali, simpan sesi untuk dipakai script scraping.

Kenapa terpisah? Shopee memaksa login untuk membuka banyak halaman ulasan,
dan sistem anti-bot-nya lebih galak kalau sesi kosong. Dengan login manual
sekali lewat script ini, cookie sesi tersimpan di folder profil persisten
(.browser_data), sehingga run scraping berikutnya tidak diminta login lagi.

Cara pakai (jalankan dari terminal supaya jendela browser muncul):
    python src/scraper/login_shopee.py

Langkah:
1. Jendela browser terbuka di halaman login Shopee.
2. Login manual sendiri (email/HP + password, atau scan QR via app Shopee),
   selesaikan OTP/captcha kalau diminta.
3. Script otomatis mendeteksi begitu kamu sudah masuk, lalu menutup browser.
   Sesi tersimpan otomatis.
"""

from __future__ import annotations

import time

from playwright.sync_api import BrowserContext, Error as PlaywrightError, Page, sync_playwright

from config import PROFILE_DIR, ambil_halaman_aktif, buka_browser
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

LOGIN_URL = "https://shopee.co.id/buyer/login"

# Berapa lama menunggu kamu login manual sebelum menyerah (detik).
BATAS_TUNGGU_DETIK = 300
# Selang antar pengecekan status login (detik).
SELANG_CEK_DETIK = 3


def sudah_login(context: BrowserContext, page: Page) -> bool:
    """Cek apakah sesi sudah dalam keadaan login.

    Args:
        context: Browser context containing persisted Shopee cookies.
        page: Current Shopee page.

    Returns:
        True when login is detected from cookies or navbar state.
    """
    # Sinyal 1: cookie user id.
    for cookie in context.cookies():
        if cookie.get("name") == "SPC_U":
            nilai = (cookie.get("value") or "").strip()
            if nilai and nilai != "-1":
                return True

    # Sinyal 2: tautan login sudah tidak ada di halaman.
    try:
        tautan_login = page.locator("a[href*='/buyer/login']")
        if page.url.rstrip("/").endswith("shopee.co.id") and tautan_login.count() == 0:
            return True
    except PlaywrightError as exc:
        logger.warning("Gagal mengecek status login dari DOM: %s", exc)

    return False


def main() -> int:
    """Run manual Shopee login flow and persist session cookies.

    Returns:
        Process exit code.
    """
    logger.info("Profil browser: %s", PROFILE_DIR)
    logger.info("Membuka halaman login Shopee")

    with sync_playwright() as p:
        context = buka_browser(p)
        page = ambil_halaman_aktif(context)

        try:
            page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60_000)

            if sudah_login(context, page):
                logger.info("Sesi sudah login dari sebelumnya, tidak perlu login lagi")
                return 0

            logger.info("Silakan login manual di jendela browser yang terbuka")
            logger.info("Selesaikan OTP/captcha kalau diminta")
            logger.info("Script menunggu maksimal %s detik", BATAS_TUNGGU_DETIK)

            tenggat = time.monotonic() + BATAS_TUNGGU_DETIK
            while time.monotonic() < tenggat:
                if sudah_login(context, page):
                    logger.info("Terdeteksi sudah login. Sesi disimpan di profil")
                    # Beri jeda singkat supaya cookie benar-benar tertulis ke disk.
                    time.sleep(2)
                    return 0
                sisa = int(tenggat - time.monotonic())
                logger.info("Menunggu login, %s detik tersisa", sisa)
                time.sleep(SELANG_CEK_DETIK)

            logger.error("Waktu habis: belum terdeteksi login. Coba jalankan lagi")
            return 1
        except PlaywrightError as exc:
            logger.exception("Gagal menjalankan proses login Shopee: %s", exc)
            return 1
        finally:
            context.close()


if __name__ == "__main__":
    raise SystemExit(main())
