import pandas as pd
import joblib
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==================================
# LOAD BOOK DATA
# ==================================

books_path = "data/Books.csv"

books = pd.read_csv(
    books_path,
    encoding="latin-1",
    on_bad_lines="skip"
)

print("Books loaded successfully!")
print("Total books:", len(books))

# ==================================
# CLEAN COLUMN NAMES
# ==================================

books.columns = books.columns.str.strip()

print("\nColumns found:")
print(books.columns)

# ==================================
# HANDLE NULL VALUES
# ==================================

for col in books.columns:
    books[col] = books[col].fillna("")

# ==================================
# CREATE COMBINED FEATURES
# ==================================

possible_columns = []

for col in books.columns:

    col_lower = col.lower()

    if (
        "title" in col_lower
        or "author" in col_lower
        or "publisher" in col_lower
    ):
        possible_columns.append(col)

print("\nUsing columns:")
print(possible_columns)

books["combined_features"] = ""

for col in possible_columns:
    books["combined_features"] += (
        books[col].astype(str) + " "
    )

# ==================================
# TF-IDF VECTORIZATION
# ==================================

vectorizer = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(
    books["combined_features"]
)

# ==================================
# COSINE SIMILARITY
# ==================================

similarity_matrix = cosine_similarity(
    tfidf_matrix
)

# ==================================
# SAVE MODEL
# ==================================

os.makedirs(
    "ml_models/saved_models",
    exist_ok=True
)

joblib.dump(
    similarity_matrix,
    "ml_models/saved_models/content_similarity.pkl"
)

joblib.dump(
    books,
    "ml_models/saved_models/books_df.pkl"
)

print("\nModel trained successfully!")
print("Saved in ml_models/saved_models/")