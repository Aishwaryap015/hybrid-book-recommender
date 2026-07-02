import pandas as pd
import os


def load_data():

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    books_path = os.path.join(BASE_DIR, 'data', 'Books.csv')
    users_path = os.path.join(BASE_DIR, 'data', 'Users.csv')
    ratings_path = os.path.join(BASE_DIR, 'data', 'Ratings.csv')

    print("📚 Loading datasets...")

    books = pd.read_csv(
        books_path,
        encoding='latin-1',
        low_memory=False
    )

    users = pd.read_csv(
        users_path,
        encoding='latin-1'
    )

    ratings = pd.read_csv(
        ratings_path,
        encoding='latin-1'
    )

    return books, users, ratings


def clean_data():

    books, users, ratings = load_data()

    print("🧹 Cleaning datasets...")

    # -------------------------
    # RENAME COLUMNS
    # -------------------------

    books = books.rename(columns={
        'ISBN': 'isbn',
        'Book-Title': 'title',
        'Book-Author': 'author',
        'Publisher': 'publisher',
        'Image-URL-M': 'image_url',
        'Publication Year': 'year'
    })

    ratings = ratings.rename(columns={
        'User-ID': 'user_id',
        'ISBN': 'isbn',
        'Book-Rating': 'rating'
    })

    users = users.rename(columns={
        'User-ID': 'user_id',
        'Location': 'location',
        'Age': 'age'
    })

    # -------------------------
    # FIX YEAR COLUMN
    # -------------------------

    if 'year' in books.columns:

        books['year'] = pd.to_numeric(
            books['year'],
            errors='coerce'
        )

    # -------------------------
    # MERGE
    # -------------------------

    data = ratings.merge(
        books,
        on='isbn'
    )

    data = data.merge(
        users,
        on='user_id',
        how='left'
    )

    # -------------------------
    # REMOVE INVALID RATINGS
    # -------------------------

    data = data[data['rating'] > 0]

    # -------------------------
    # REMOVE DUPLICATES
    # -------------------------

    data = data.drop_duplicates(
        subset=['user_id', 'title']
    )

    # -------------------------
    # ACTIVE USERS
    # -------------------------

    user_counts = data['user_id'].value_counts()

    active_users = user_counts[
        user_counts >= 50
    ].index

    data = data[
        data['user_id'].isin(active_users)
    ]

    # -------------------------
    # POPULAR BOOKS
    # -------------------------

    book_counts = data['title'].value_counts()

    popular_books = book_counts[
        book_counts >= 20
    ].index

    data = data[
        data['title'].isin(popular_books)
    ]

    # -------------------------
    # CLEAN NULLS
    # -------------------------

    data['title'] = data['title'].fillna('Unknown')
    data['author'] = data['author'].fillna('Unknown')
    data['publisher'] = data['publisher'].fillna('Unknown')

    print("✅ Final cleaned data shape:", data.shape)

    return data


if __name__ == "__main__":

    df = clean_data()

    print(df.head())