"""Konfigurasi & utilitas bersama untuk scraper Shopee.

Semua script scraper (login, test, pengambilan ulasan) memakai pengaturan
yang sama dari sini supaya konsisten: profil browser, user-agent, jeda acak,
dan cara meluncurkan browser.
"""

from __future__ import annotations

import random
import sys
import time
from pathlib import Path

from playwright.sync_api import BrowserContext, Page, Playwright

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logging_config import get_logger  # noqa: E402

logger = get_logger(__name__)

# Homepage Shopee Indonesia.
HOME_URL = "https://shopee.co.id/"

# User agent desktop yang wajar, biar tidak gampang dicurigai sebagai bot.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# Folder penyimpanan profil browser (cookie, sesi login) supaya persisten.
# Letaknya di root proyek: <root>/.browser_data
PROFILE_DIR = Path(__file__).resolve().parents[2] / ".browser_data"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PRODUCTS_FILE = PROJECT_ROOT / "src" / "products.txt"
RAW_REVIEWS_FILE = RAW_DATA_DIR / "dataset_ulasan_mentah.csv"


def jeda(min_detik: float = 1.0, maks_detik: float = 3.0) -> None:
    """Sleep for a random duration to reduce rigid access patterns.

    Args:
        min_detik: Minimum sleep duration in seconds.
        maks_detik: Maximum sleep duration in seconds.
    """
    waktu = random.uniform(min_detik, maks_detik)
    logger.info("Jeda %.1f detik", waktu)
    time.sleep(waktu)


def buka_browser(p: Playwright) -> BrowserContext:
    """Luncurkan Chromium dengan profil persisten & pengaturan anti-deteksi.

    Args:
        p: Playwright runtime instance.

    Returns:
        Persistent Chromium browser context shared by scraper scripts.
    """
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    return p.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
        user_agent=USER_AGENT,
        viewport={"width": 1366, "height": 768},
        locale="id-ID",
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ],
    )


def ambil_halaman_aktif(context: BrowserContext) -> Page:
    """Return the existing browser page or create one when none exists.

    Args:
        context: Persistent browser context.

    Returns:
        Active Playwright page for the scraper script.
    """
    return context.pages[0] if context.pages else context.new_page()
