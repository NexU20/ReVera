"""Scrape raw Shopee reviews with Playwright.

This module only handles data extraction and raw CSV generation. Text
cleaning, sentiment classification, and aspect tagging belong to the
preprocessing/model/tagging modules.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil
from pathlib import Path

import pandas as pd
from playwright.sync_api import (
    ElementHandle,
    Error as PlaywrightError,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from config import (
    PRODUCTS_FILE,
    RAW_REVIEWS_FILE,
    ambil_halaman_aktif,
    buka_browser,
    jeda,
)
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

MAX_REVIEWS_PER_PRODUK = 120
MAX_REVIEW_PAGES_PER_FILTER = 20
MAX_STAGNANT_PAGES = 2
RATING_FILTERS = (1, 2, 3, 4, 5)
REVIEW_SECTION_SELECTOR = "div.shopee-product-comment-list"
REVIEW_ITEM_SELECTOR = "div[data-cmtid]"
NEXT_BUTTON_SELECTOR = "button.shopee-icon-button--right"
RATING_FILTER_SELECTOR = "div.product-rating-overview__filter"
AUTHOR_SELECTOR = ":scope > div:nth-child(2) > div:nth-child(1) > a"
CONTENT_SELECTOR = ":scope > div:nth-child(2) > div:nth-child(2)"
STAR_SELECTOR = "svg.icon-rating-solid"
DISABLED_NEXT_CLASS = "shopee-button-no-outline--non-click"


@dataclass(frozen=True)
class ShopeeReview:
    """Raw Shopee review record extracted from the product review DOM."""

    id_komentar: str
    produk_url: str
    username: str
    rating: int
    ulasan: str


def read_product_urls(file_path: Path = PRODUCTS_FILE) -> list[str]:
    """Read Shopee product URLs from a text file.

    Args:
        file_path: Text file containing one product URL per line.

    Returns:
        Non-empty product URLs.

    Raises:
        FileNotFoundError: If the product URL file does not exist.
    """
    with file_path.open("r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def normalize_review_text(text: str) -> str:
    """Normalize raw multiline review text for CSV storage.

    Args:
        text: Raw text extracted from a Shopee review element.

    Returns:
        Review text with line breaks collapsed.
    """
    return " | ".join(part.strip() for part in text.splitlines() if part.strip())


def extract_review(
    review_element: ElementHandle,
    product_url: str,
    seen_review_ids: set[str],
) -> ShopeeReview | None:
    """Extract one review record from a review element.

    Args:
        review_element: Playwright element containing one Shopee review.
        product_url: Product URL currently being scraped.
        seen_review_ids: Review IDs already emitted in this scrape run.

    Returns:
        A raw review record, or None when the element is duplicate/incomplete.
    """
    comment_id = review_element.get_attribute("data-cmtid")
    if not comment_id or comment_id in seen_review_ids:
        return None

    author_element = review_element.query_selector(AUTHOR_SELECTOR)
    content_element = review_element.query_selector(CONTENT_SELECTOR)
    review_text = (
        normalize_review_text(content_element.inner_text()) if content_element else ""
    )

    if not review_text:
        return None

    username = author_element.inner_text().strip() if author_element else "Anonim"
    rating = len(review_element.query_selector_all(STAR_SELECTOR))

    return ShopeeReview(
        id_komentar=comment_id,
        produk_url=product_url,
        username=username,
        rating=rating,
        ulasan=review_text,
    )


def scroll_to_review_section(page: Page, scroll_count: int = 8) -> None:
    """Scroll down to trigger lazy loading of the review section.

    Args:
        page: Product page.
        scroll_count: Number of mouse wheel scrolls.
    """
    logger.info("Menggulir ke bawah untuk memuat ulasan")
    for _ in range(scroll_count):
        page.mouse.wheel(0, 800)
        jeda(0.8, 1.2)


def wait_for_reviews(page: Page) -> bool:
    """Wait until Shopee review section appears.

    Args:
        page: Product page.

    Returns:
        True when the review section is found.
    """
    try:
        page.wait_for_selector(REVIEW_SECTION_SELECTOR, timeout=15_000)
        return True
    except PlaywrightTimeoutError as exc:
        logger.warning("Gagal menemukan section ulasan: %s", exc)
        return False


def select_review_filter(page: Page, filter_text: str) -> bool:
    """Select a Shopee review filter by visible text.

    Args:
        page: Product page.
        filter_text: Visible text contained by the target filter.

    Returns:
        True when the filter was clicked successfully.
    """
    filter_button = page.locator(RATING_FILTER_SELECTOR).filter(has_text=filter_text)

    try:
        if filter_button.count() == 0:
            logger.warning("Filter %s tidak ditemukan", filter_text)
            return False

        filter_button.first.scroll_into_view_if_needed()
        jeda(0.8, 1.2)
        filter_button.first.click()
        jeda(2.0, 3.0)
        return wait_for_reviews(page)
    except PlaywrightTimeoutError as exc:
        logger.warning("Timeout saat memilih filter %s: %s", filter_text, exc)
        return False
    except PlaywrightError as exc:
        logger.warning("Gagal memilih filter %s: %s", filter_text, exc)
        return False


def select_rating_filter(page: Page, rating: int) -> bool:
    """Select Shopee review filter for a specific star rating.

    Args:
        page: Product page.
        rating: Star rating to select, from 1 to 5.

    Returns:
        True when the rating filter was clicked successfully.
    """
    return select_review_filter(page, f"{rating} bintang")


def select_all_reviews_filter(page: Page) -> bool:
    """Select Shopee review filter for all ratings.

    Args:
        page: Product page.

    Returns:
        True when the all-reviews filter was clicked successfully.
    """
    return select_review_filter(page, "Semua")


def is_next_button_disabled(next_button: ElementHandle) -> bool:
    """Check whether the Shopee review next-page button is disabled.

    Args:
        next_button: Pagination next button element.

    Returns:
        True when the button cannot be clicked.
    """
    button_classes = next_button.get_attribute("class") or ""
    return (
        next_button.get_attribute("disabled") is not None
        or DISABLED_NEXT_CLASS in button_classes
    )


def go_to_next_review_page(page: Page) -> bool:
    """Click the review pagination next button when available.

    Args:
        page: Product page.

    Returns:
        True when navigation to the next review page was attempted.
    """
    next_button = page.query_selector(NEXT_BUTTON_SELECTOR)
    if next_button is None:
        logger.info("Tombol next tidak ditemukan. Menghentikan produk ini")
        return False

    if is_next_button_disabled(next_button):
        logger.info("Halaman terakhir ulasan telah dicapai")
        return False

    next_button.scroll_into_view_if_needed()
    jeda(0.8, 1.2)
    next_button.evaluate("button => button.click()")
    jeda(3.0, 4.0)
    return True


def collect_visible_reviews(
    page: Page,
    product_url: str,
    seen_review_ids: set[str],
    max_reviews: int,
    rating_filter: int | None = None,
) -> list[ShopeeReview]:
    """Collect reviews from the currently selected review filter.

    Args:
        page: Product page with a review filter already selected.
        product_url: Shopee product URL.
        seen_review_ids: Global review IDs already emitted in this run.
        max_reviews: Maximum reviews to collect from the current filter.
        rating_filter: Selected star rating, or None for Shopee default filter.

    Returns:
        Raw review records from the visible review list.
    """
    collected_reviews: list[ShopeeReview] = []
    page_number = 1
    stagnant_pages = 0

    while (
        len(collected_reviews) < max_reviews
        and page_number <= MAX_REVIEW_PAGES_PER_FILTER
        and stagnant_pages < MAX_STAGNANT_PAGES
    ):
        logger.info(
            "Mengekstrak halaman ulasan %s untuk filter %s",
            page_number,
            f"{rating_filter} bintang" if rating_filter else "default",
        )
        jeda(1.5, 2.5)
        reviews_before_page = len(collected_reviews)

        review_elements = page.query_selector_all(REVIEW_ITEM_SELECTOR)
        if not review_elements:
            logger.info("Tidak ada elemen ulasan pada halaman ini")
            break

        for review_element in review_elements:
            if len(collected_reviews) >= max_reviews:
                logger.info("Batas maksimal %s ulasan filter ini tercapai", max_reviews)
                break

            review = extract_review(review_element, product_url, seen_review_ids)
            if review is None:
                continue

            if rating_filter is not None and review.rating != rating_filter:
                logger.warning(
                    "Review %s punya rating %s, bukan filter %s",
                    review.id_komentar,
                    review.rating,
                    rating_filter,
                )
                continue

            collected_reviews.append(review)
            seen_review_ids.add(review.id_komentar)

        if len(collected_reviews) == reviews_before_page:
            stagnant_pages += 1
            logger.info(
                "Tidak ada review baru pada halaman ini. Stagnasi %s/%s",
                stagnant_pages,
                MAX_STAGNANT_PAGES,
            )
        else:
            stagnant_pages = 0

        logger.info("Terkumpul %s ulasan dari filter ini", len(collected_reviews))

        if len(collected_reviews) >= max_reviews or not go_to_next_review_page(page):
            break
        page_number += 1

    if page_number > MAX_REVIEW_PAGES_PER_FILTER:
        logger.warning(
            "Batas %s halaman tercapai untuk filter %s",
            MAX_REVIEW_PAGES_PER_FILTER,
            f"{rating_filter} bintang" if rating_filter else "default",
        )

    return collected_reviews


def scrape_product_reviews(
    page: Page,
    product_url: str,
    seen_review_ids: set[str],
    max_reviews: int = MAX_REVIEWS_PER_PRODUK,
) -> list[ShopeeReview]:
    """Scrape balanced raw reviews for one Shopee product URL.

    Args:
        page: Reusable Playwright page.
        product_url: Shopee product URL.
        seen_review_ids: Global review IDs already emitted in this run.
        max_reviews: Maximum reviews to collect from this product.

    Returns:
        Raw review records extracted from the product.
    """
    logger.info("Membuka produk: %s", product_url)
    product_reviews: list[ShopeeReview] = []

    try:
        page.goto(product_url, wait_until="domcontentloaded", timeout=60_000)
        jeda(2.5, 3.5)
        scroll_to_review_section(page)

        if not wait_for_reviews(page):
            return product_reviews

        max_reviews_per_rating = ceil(max_reviews / len(RATING_FILTERS))
        for rating in RATING_FILTERS:
            if len(product_reviews) >= max_reviews:
                break

            if not select_rating_filter(page, rating):
                continue

            remaining_quota = max_reviews - len(product_reviews)
            rating_quota = min(max_reviews_per_rating, remaining_quota)
            product_reviews.extend(
                collect_visible_reviews(
                    page=page,
                    product_url=product_url,
                    seen_review_ids=seen_review_ids,
                    max_reviews=rating_quota,
                    rating_filter=rating,
                )
            )

        if not product_reviews:
            logger.warning(
                "Filter rating tidak menghasilkan data. Menggunakan daftar ulasan default"
            )
            select_all_reviews_filter(page)
            product_reviews.extend(
                collect_visible_reviews(
                    page=page,
                    product_url=product_url,
                    seen_review_ids=seen_review_ids,
                    max_reviews=max_reviews,
                )
            )

        rating_counts = pd.Series([review.rating for review in product_reviews]).value_counts()
        logger.info("Distribusi rating produk ini: %s", rating_counts.to_dict())

    except PlaywrightTimeoutError as exc:
        logger.error("Timeout saat memuat produk %s: %s", product_url, exc)
    except PlaywrightError as exc:
        logger.exception("Gagal scraping produk %s: %s", product_url, exc)

    return product_reviews


def save_reviews(
    reviews: list[ShopeeReview], output_path: Path = RAW_REVIEWS_FILE
) -> None:
    """Save raw reviews to CSV.

    Args:
        reviews: Raw Shopee review records.
        output_path: Destination CSV path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(asdict(review) for review in reviews)
    dataframe.to_csv(output_path, index=False, encoding="utf-8")
    logger.info("%s ulasan berhasil disimpan ke %s", len(reviews), output_path)


def scrape_reviews() -> int:
    """Scrape configured Shopee products and write raw review CSV.

    Returns:
        Process exit code.
    """
    try:
        product_urls = read_product_urls()
    except FileNotFoundError as exc:
        logger.error("File products.txt tidak ditemukan: %s", exc)
        return 1

    logger.info("Ditemukan %s produk untuk discrape", len(product_urls))
    all_reviews: list[ShopeeReview] = []
    seen_review_ids: set[str] = set()

    with sync_playwright() as playwright:
        context = buka_browser(playwright)
        page = ambil_halaman_aktif(context)
        try:
            for product_url in product_urls:
                all_reviews.extend(
                    scrape_product_reviews(page, product_url, seen_review_ids)
                )
                jeda(3.5, 4.5)
        finally:
            context.close()

    if not all_reviews:
        logger.warning("Tidak ada ulasan yang berhasil diekstrak")
        return 1

    save_reviews(all_reviews)
    return 0


if __name__ == "__main__":
    raise SystemExit(scrape_reviews())
