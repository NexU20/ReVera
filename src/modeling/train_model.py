"""Train and evaluate sentiment classification models.

This module implements the full ML modeling pipeline:
1. Load cleaned dataset
2. TF-IDF feature extraction
3. Train/Test split (80:20)
4. Train SVM + Naive Bayes + Logistic Regression
5. Evaluate with Confusion Matrix, Accuracy, F1-Score
6. Save best model + vectorizer to disk (.joblib)
"""

from __future__ import annotations

import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

INPUT_PATH = Path("data/processed/dataset_cleaned.csv")
MODELS_DIR = Path("models")
LABEL_NAMES = ["Negatif", "Netral", "Positif"]


def load_dataset(path: Path = INPUT_PATH) -> tuple[pd.Series, pd.Series]:
    """Load cleaned dataset and return text features + labels.

    Returns:
        Tuple of (X: ulasan_bersih, y: label_encoded).
    """
    try:
        df = pd.read_csv(path)
        logger.info("Dataset dimuat: %d baris", len(df))
    except Exception as e:
        logger.error("Gagal memuat dataset: %s", e)
        raise

    # Pastikan tidak ada NaN di kolom kritis
    df = df.dropna(subset=["ulasan_bersih", "label_encoded"])
    df["ulasan_bersih"] = df["ulasan_bersih"].astype(str)
    df["label_encoded"] = df["label_encoded"].astype(int)

    logger.info("Distribusi label:")
    for label_id, name in enumerate(LABEL_NAMES):
        count = (df["label_encoded"] == label_id).sum()
        logger.info("  %s (%d): %d", name, label_id, count)

    return df["ulasan_bersih"], df["label_encoded"]


def build_tfidf(X_train: pd.Series) -> TfidfVectorizer:
    """Fit a TF-IDF vectorizer on training data.

    Args:
        X_train: Training text data.

    Returns:
        Fitted TfidfVectorizer.
    """
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),  # unigram + bigram
        min_df=2,
        max_df=0.95,
    )
    vectorizer.fit(X_train)
    logger.info(
        "TF-IDF fitted: %d fitur (vocab size)", len(vectorizer.vocabulary_)
    )
    return vectorizer


def train_and_evaluate(
    X_train,
    X_test,
    y_train,
    y_test,
) -> dict:
    """Train multiple classifiers and return evaluation results.

    Returns:
        Dict mapping model_name -> {model, accuracy, f1, report, cm}.
    """
    models = {
        "SVM (LinearSVC)": LinearSVC(
            class_weight="balanced",
            max_iter=10000,
            random_state=42,
        ),
        "Naive Bayes": MultinomialNB(alpha=1.0),
        "Logistic Regression": LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
        ),
    }

    results = {}

    for name, model in models.items():
        logger.info("Melatih model: %s ...", name)
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted")
            report = classification_report(
                y_test, y_pred, target_names=LABEL_NAMES
            )
            cm = confusion_matrix(y_test, y_pred)

            results[name] = {
                "model": model,
                "accuracy": acc,
                "f1_score": f1,
                "report": report,
                "confusion_matrix": cm,
            }

            logger.info("  Accuracy : %.4f", acc)
            logger.info("  F1-Score : %.4f", f1)
            logger.info("\n%s", report)

        except Exception as e:
            logger.error("Gagal melatih %s: %s", name, e)

    return results


def save_best_model(
    results: dict,
    vectorizer: TfidfVectorizer,
    output_dir: Path = MODELS_DIR,
) -> str:
    """Save the best performing model and its TF-IDF vectorizer.

    Args:
        results: Evaluation results dict from train_and_evaluate.
        vectorizer: Fitted TfidfVectorizer.
        output_dir: Directory to store model artifacts.

    Returns:
        Name of the best model.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Pick model with highest F1-Score
    best_name = max(results, key=lambda k: results[k]["f1_score"])
    best_model = results[best_name]["model"]

    model_path = output_dir / "best_model.joblib"
    vectorizer_path = output_dir / "tfidf_vectorizer.joblib"

    try:
        joblib.dump(best_model, model_path)
        joblib.dump(vectorizer, vectorizer_path)
        logger.info("Model terbaik '%s' disimpan ke %s", best_name, model_path)
        logger.info("TF-IDF Vectorizer disimpan ke %s", vectorizer_path)
    except Exception as e:
        logger.error("Gagal menyimpan model: %s", e)

    return best_name


def run_pipeline():
    """Execute the full modeling pipeline."""
    # 1. Load dataset
    X, y = load_dataset()

    # 2. Train/Test Split (80:20, stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    logger.info("Train: %d, Test: %d", len(X_train), len(X_test))

    # 3. TF-IDF Vectorization
    vectorizer = build_tfidf(X_train)
    X_train_tfidf = vectorizer.transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # 4. Train & Evaluate
    results = train_and_evaluate(X_train_tfidf, X_test_tfidf, y_train, y_test)

    # 5. Save best model
    best_name = save_best_model(results, vectorizer)

    # 6. Summary
    logger.info("\n" + "=" * 60)
    logger.info("RINGKASAN PERBANDINGAN MODEL")
    logger.info("=" * 60)
    for name, res in results.items():
        marker = " ← TERBAIK" if name == best_name else ""
        logger.info(
            "  %-25s | Acc: %.4f | F1: %.4f%s",
            name, res["accuracy"], res["f1_score"], marker,
        )
    logger.info("=" * 60)


if __name__ == "__main__":
    run_pipeline()
