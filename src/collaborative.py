import pandas as pd
import numpy as np

def get_collaborative_recommendations(user_id, ratings_df, books_df):
    # 1. Filter out inactive users to avoid sparse matrix issues
    user_counts = ratings_df['User-ID'].value_counts()
    active_users = user_counts[user_counts >= 50].index
    filtered_ratings = ratings_df[ratings_df['User-ID'].isin(active_users)]

    # 2. Pivot Table: User-Item Matrix
    # Using 'ISBN' as the primary key from your ratings.csv
    user_item_matrix = filtered_ratings.pivot_table(index='User-ID', columns='ISBN', values='Book-Rating').fillna(0)

    # 3. Pearson Correlation Calculation
    # We transpose to get item-item similarity based on user ratings
    item_similarity_matrix = user_item_matrix.corr(method='pearson')

    return item_similarity_matrix