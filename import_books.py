import pandas as pd
from pymongo import MongoClient

# =========================================================
# CONNECT TO MONGODB
# =========================================================

client = MongoClient("mongodb://localhost:27017/")

db = client["bookai"]

books_collection = db["books"]

# =========================================================
# LOAD CSV FILE
# =========================================================

df = pd.read_csv(
    "data/Books.csv",
    low_memory=False
)

print(df.columns.tolist())

# =========================================================
# CLEAR OLD BOOKS
# =========================================================

books_collection.delete_many({})

books = []

# =========================================================
# CATEGORY DETECTION FUNCTION
# =========================================================

def detect_category(title):

    title = str(title).lower()

    # =====================================
    # MYSTERY
    # =====================================

    if any(word in title for word in [

        "mystery",
        "detective",
        "secret",
        "shadow",
        "dark"
    ]):

        return "mystery"

    # =====================================
    # CRIME
    # =====================================

    if any(word in title for word in [

        "crime",
        "killer",
        "murder",
        "criminal",
        "death"
    ]):

        return "crime"

    # =====================================
    # LEADERSHIP
    # =====================================

    if any(word in title for word in [

        "leader",
        "leadership",
        "success",
        "business",
        "management"
    ]):

        return "leadership"

    # =====================================
    # MYTHOLOGY
    # =====================================

    if any(word in title for word in [

        "god",
        "legend",
        "mythology",
        "ramayana",
        "mahabharata"
    ]):

        return "mythology"

    # =====================================
    # CHILDREN
    # =====================================

    if any(word in title for word in [

        "children",
        "kids",
        "fairy",
        "magic",
        "wizard",
        "child"
    ]):

        return "children"

    # =====================================
    # ROMANCE
    # =====================================

    if any(word in title for word in [

        "love",
        "romance",
        "heart",
        "kiss",
        "relationship"
    ]):

        return "romance"

    # =====================================
    # OLD AGE
    # =====================================

    if any(word in title for word in [

        "old",
        "elder",
        "grandfather",
        "grandmother",
        "aging",
        "retirement",
        "senior"
    ]):

        return "old_age"

    # =====================================
    # STRUGGLE JOURNEY
    # =====================================

    if any(word in title for word in [

        "journey",
        "struggle",
        "life",
        "dream",
        "survival",
        "war",
        "hope",
        "fight",
        "adventure"
    ]):

        return "struggle_journey"

    # =====================================
    # FICTION
    # =====================================

    if any(word in title for word in [

        "story",
        "novel",
        "fiction",
        "chronicles"
    ]):

        return "fiction"

    # =====================================
    # DEFAULT
    # =====================================

    return "general"

# =========================================================
# IMPORT BOOKS
# =========================================================

for index, row in df.iterrows():

    try:

        title = str(
            row["Title"]
        ).strip()

        author = str(
            row["Author"]
        ).strip()

        isbn = str(
            row["ISBN"]
        ).strip()

        raw_image = str(
            row["Image-URL"]
        ).strip()

        rating = float(
            row.get("AvgRating", 0)
        )

        # =====================================
        # IMAGE HANDLING
        # =====================================

        if raw_image.startswith("http"):

            image_url = (
                f"https://images.weserv.nl/?url={raw_image}"
            )

        else:

            image_url = "/static/fallback-book.png"

        # =====================================
        # CREATE BOOK DOCUMENT
        # =====================================

        books.append({

            "id": index + 1,

            "isbn": isbn,

            "title": title,

            "author": author,

            "image_url": image_url,

            "category": detect_category(title),

            "language": "english",

            "format": "book",

            "rating": rating
        })

    except Exception as e:

        print(
            f"Error importing row {index}: {e}"
        )

# =========================================================
# INSERT INTO MONGODB
# =========================================================

if books:

    books_collection.insert_many(books)

    print(
        f"{len(books)} Books Imported Successfully!"
    )

else:

    print("No books imported.")