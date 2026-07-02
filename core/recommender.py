import os
import joblib
import pandas as pd


class BookRecommender:

    def __init__(self):

        self.books_df = None
        self.knn_model = None
        self.user_item_matrix = None

        self.load_saved_models()

    # ==================================
    # LOAD TRAINED MODELS
    # ==================================

    def load_saved_models(self):

        try:

            base_dir = os.path.dirname(
                os.path.dirname(__file__)
            )

            model_path = os.path.join(
                base_dir,
                "ml_models",
                "saved_models"
            )

            print(
                "Loading trained ML model..."
            )

            self.books_df = joblib.load(
                os.path.join(
                    model_path,
                    "books_df.pkl"
                )
            )

            self.knn_model = joblib.load(
                os.path.join(
                    model_path,
                    "knn_model.pkl"
                )
            )

            self.user_item_matrix = joblib.load(
                os.path.join(
                    model_path,
                    "user_item_matrix.pkl"
                )
            )

            print(
                "ML model loaded successfully!"
            )

            print(
                "Columns in books_df:",
                self.books_df.columns
            )

        except Exception as e:

            print(
                "Model loading error:",
                str(e)
            )

    # ==================================
    # GET RECOMMENDATIONS
    # ==================================

    def get_recommendations(
        self,
        book_title,
        book_isbn=None,
        num_books=8
    ):

        try:

            title_column = "Title"
            isbn_column = "ISBN"

            matching_books = pd.DataFrame()

            # ==================================
            # ISBN MATCH
            # ==================================

            if (
                book_isbn
                and
                isbn_column in self.books_df.columns
            ):

                matching_books = self.books_df[

                    self.books_df[
                        isbn_column
                    ]
                    .astype(str)

                    ==

                    str(book_isbn)
                ]

            # ==================================
            # TITLE MATCH
            # ==================================

            if matching_books.empty:

                matching_books = self.books_df[

                    self.books_df[
                        title_column
                    ]
                    .astype(str)
                    .str.lower()

                    ==

                    book_title.lower()
                ]

            if matching_books.empty:

                print(
                    "BOOK NOT FOUND:",
                    book_title
                )

                return []

            book_index = (
                matching_books.index[0]
            )

            distances, indices = (

                self.knn_model.kneighbors(

                    self.user_item_matrix
                    .iloc[book_index]
                    .values
                    .reshape(1, -1),

                    n_neighbors=num_books + 1
                )
            )

            recommended_titles = []

            for idx in indices.flatten():

                if idx != book_index:

                    title = (

                        self.books_df
                        .iloc[idx][
                            title_column
                        ]
                    )

                    recommended_titles.append(
                        title
                    )

            print(
                "RECOMMENDATIONS:",
                recommended_titles
            )

            return recommended_titles

        except Exception as e:

            print(
                "Recommendation error:",
                str(e)
            )

            return []