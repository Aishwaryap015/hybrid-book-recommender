import os
import sys
import django
import pandas as pd

# Setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_engine.settings')
django.setup()

from core.models import Book, Rating, DoodleUser

def import_ratings():
    # Path to your ratings file
    csv_path = os.path.join(BASE_DIR, 'data', 'Ratings.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join(BASE_DIR, 'Ratings.csv')

    print("Loading Ratings...")
    # Loading first 5000 ratings to keep your ThinkPad fast
    df = pd.read_csv(csv_path).head(5000) 

    # We need at least one user to assign these ratings to
    # Checking if 'admin' exists, otherwise creating a test user
    user, created = DoodleUser.objects.get_or_create(username='test_user')

    print(f"Processing {len(df)} ratings...")
    count = 0
    for _, row in df.iterrows():
        try:
            # Find the book by ISBN
            book = Book.objects.get(isbn=row['ISBN'])
            
            # Create the rating
            Rating.objects.get_or_create(
                user=user,
                book=book,
                defaults={'rating': int(row['Book-Rating'])}
            )
            count += 1
            if count % 100 == 0:
                print(f"Linked {count} ratings...")
        except Book.DoesNotExist:
            # Skip ratings for books we haven't imported yet
            continue

    print(f"Success! Linked {count} ratings to your books.")

if __name__ == "__main__":
    import_ratings()