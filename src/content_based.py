import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def create_features(data):

    # Fill missing values safely
    data['title'] = data['title'].fillna('')
    data['author'] = data['author'].fillna('')
    data['publisher'] = data['publisher'].fillna('')

    # Feature Engineering
    data['features'] = (
        data['title'].astype(str).str.lower() + " " +
        data['author'].astype(str).str.lower() + " " +
        data['publisher'].astype(str).str.lower()
    )

    return data


def compute_similarity(data):

    tfidf = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2)
    )

    tfidf_matrix = tfidf.fit_transform(data['features'])

    similarity = cosine_similarity(tfidf_matrix)

    return similarity


def recommend_books(title, data, similarity, n=5):

    if title not in data['title'].values:
        print("❌ Book not found")
        return []

    idx = data[data['title'] == title].index[0]

    scores = list(enumerate(similarity[idx]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []
    seen = set()

    for i in scores[1:50]:

        book = data.iloc[i[0]]['title']

        if book not in seen:
            recommendations.append(book)
            seen.add(book)

        if len(recommendations) >= n:
            break

    return recommendations


if __name__ == "__main__":

    from data_preprocessing import clean_data

    data = clean_data()

    data = create_features(data)

    similarity = compute_similarity(data)

    sample_book = data['title'].iloc[0]

    print("📚 Testing for:", sample_book)

    recs = recommend_books(
        sample_book,
        data,
        similarity
    )

    print(recs)