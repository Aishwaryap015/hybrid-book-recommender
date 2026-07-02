import pandas as pd


def hybrid_recommend(user_id, title, matrix, user_similarity, content_data, content_similarity, n=5):
    
    # -------------------------------
    # 1. Collaborative part
    # -------------------------------
    collab_scores = pd.Series(dtype=float)

    if user_id in matrix.index:
        similar_users = user_similarity[user_id].sort_values(ascending=False)[1:6]

        similar_users_ratings = matrix.loc[similar_users.index]
        collab_scores = similar_users_ratings.mean().sort_values(ascending=False)

        # Remove already rated books
        user_books = matrix.loc[user_id].dropna().index
        collab_scores = collab_scores.drop(user_books, errors='ignore')

    # -------------------------------
    # 2. Content-based part
    # -------------------------------
    content_scores = pd.Series(dtype=float)

    if title in content_data['title'].values:
        idx = content_data[content_data['title'] == title].index[0]

        scores = list(enumerate(content_similarity[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        content_list = []
        seen = set()

        for i in scores[1:50]:
            book = content_data.iloc[i[0]]['title']

            if book not in seen:
                content_list.append(book)
                seen.add(book)

            if len(content_list) >= 20:
                break

        content_scores = pd.Series(range(len(content_list), 0, -1), index=content_list)

    # -------------------------------
    # 3. Hybrid merge (SMART PART 🔥)
    # -------------------------------
    hybrid_scores = pd.Series(dtype=float)

    # Weighting (you can explain this in viva)
    alpha = 0.7   # collaborative weight
    beta = 0.3    # content weight

    for book in collab_scores.index:
        hybrid_scores[book] = hybrid_scores.get(book, 0) + alpha * collab_scores[book]

    for book in content_scores.index:
        hybrid_scores[book] = hybrid_scores.get(book, 0) + beta * content_scores[book]

    # Sort final recommendations
    hybrid_scores = hybrid_scores.sort_values(ascending=False)

    print("\n🔥 Hybrid Recommendations:\n")
    print(hybrid_scores.head(n))


# -----------------------------------
# TESTING
# -----------------------------------
if __name__ == "__main__":
    from data_preprocessing import clean_data
    from collaborative import create_user_item_matrix, pearson_similarity
    from content_based import create_features, compute_similarity

    data = clean_data()

    # Collaborative setup
    matrix = create_user_item_matrix(data)
    user_similarity = pearson_similarity(matrix)

    # Content setup
    content_data = create_features(data)
    content_similarity = compute_similarity(content_data)

    # Test
    user = matrix.index[0]
    book = data['title'].iloc[0]

    print("User:", user)
    print("Book:", book)

    hybrid_recommend(user, book, matrix, user_similarity, content_data, content_similarity)