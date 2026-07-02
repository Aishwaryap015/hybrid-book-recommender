import os
import sys
import django
import pandas as pd

# 1. Setup paths so Django can find your project settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 2. Point to your specific settings folder (book_engine)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_engine.settings')
django.setup()

# 3. Import your model after django.setup()
from core.models import Book

def import_books():
    # Find the CSV file in /data or root
    csv_path = os.path.join(BASE_DIR, 'data', 'Books.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join(BASE_DIR, 'Books.csv')

    if not os.path.exists(csv_path):
        print(f"Error: Could not find Books.csv at {csv_path}")
        return

    print(f"Reading CSV from: {csv_path}")
    
    # Load the data
    try:
        df = pd.read_csv(csv_path)
        total_rows = len(df)
        print(f"Starting import of {total_rows} books...")

        # 4. The main loop with Progress Tracker
        for index, row in df.iterrows():
            # This logic ensures we don't create the same book twice
            Book.objects.update_or_create(
                isbn=row['ISBN'], 
                defaults={
                    'title': row['Title'],
                    'author': row['Author'],
                    'year': str(row['Publication Year']),
                    'image_url': row['Image-URL'],
                    'average_rating': float(row['AvgRating']) if pd.notnull(row['AvgRating']) else 0.0
                }
            )

            # Progress Tracker: Prints every 50 books so the terminal doesn't freeze
            if index % 50 == 0:
                print(f"Progress: [{index}/{total_rows}] books processed...")

        print("\nSuccess! Import completed. All books are now in the database.")
        print(f"Total books in DB: {Book.objects.count()}")

    except Exception as e:
        print(f"An error occurred during import: {e}")

if __name__ == "__main__":
    import_books()