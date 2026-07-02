import pandas as pd
import numpy as np
import joblib
import os

from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity

# ==================================
# LOAD RATINGS
# ==================================

ratings = pd.read_csv(
    "data/Ratings.csv",
    encoding="latin-1",
    on_bad_lines="skip"
)

print("Ratings loaded!")
print("Total ratings:", len(ratings))

# ==================================
# CLEAN DATA
# ==================================

ratings.columns = ratings.columns.str.strip()

ratings["Book-Rating"] = pd.to_numeric(
    ratings["Book-Rating"],
    errors="coerce"
)

ratings.dropna(inplace=True)

# ==================================
# FILTER ACTIVE USERS
# ==================================

user_counts = ratings["User-ID"].value_counts()

active_users = user_counts[
    user_counts >= 50
].index

ratings = ratings[
    ratings["User-ID"].isin(active_users)
]

print("\nAfter active user filtering:")
print(len(ratings))

# ==================================
# FILTER POPULAR BOOKS
# ==================================

book_counts = ratings["ISBN"].value_counts()

popular_books = book_counts[
    book_counts >= 20
].index

ratings = ratings[
    ratings["ISBN"].isin(popular_books)
]

print("\nAfter popular book filtering:")
print(len(ratings))

# ==================================
# CREATE USER-ITEM MATRIX
# ==================================

user_item_matrix = ratings.pivot_table(
    index="User-ID",
    columns="ISBN",
    values="Book-Rating",
    fill_value=0
)

print("\nUser-item matrix created!")
print(user_item_matrix.shape)

# ==================================
# TRAIN KNN
# ==================================

knn_model = NearestNeighbors(
    metric="cosine",
    algorithm="brute",
    n_neighbors=10
)

knn_model.fit(user_item_matrix)

print("\nKNN trained!")

# ==================================
# PEARSON CORRELATION
# ==================================

pearson_similarity = (
    user_item_matrix.T.corr(method="pearson")
)

print("Pearson similarity created!")

# ==================================
# CENTERED COSINE
# ==================================

mean_user_rating = (
    user_item_matrix.mean(axis=1)
)

centered_matrix = (
    user_item_matrix.sub(
        mean_user_rating,
        axis=0
    )
)

centered_cosine = cosine_similarity(
    centered_matrix
)

print("Centered cosine created!")

# ==================================
# SAVE MODELS
# ==================================

os.makedirs(
    "ml_models/saved_models",
    exist_ok=True
)

joblib.dump(
    knn_model,
    "ml_models/saved_models/knn_model.pkl"
)

joblib.dump(
    pearson_similarity,
    "ml_models/saved_models/pearson_similarity.pkl"
)

joblib.dump(
    centered_cosine,
    "ml_models/saved_models/centered_cosine.pkl"
)

joblib.dump(
    user_item_matrix,
    "ml_models/saved_models/user_item_matrix.pkl"
)

print("\nSUCCESS!")
print("Collaborative model trained.")