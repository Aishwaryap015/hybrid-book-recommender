import logging
import os
import json
import random
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, session, redirect, jsonify, url_for
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- ⚙️ CONFIG & LOGGING ---
# Suppress unnecessary console logs to keep your terminal clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) 

app = Flask(__name__)
app.secret_key = "doodle_secret_321"

# --- 💾 DATA & NEURAL ENGINE ---
def initialize_engine():
    """Initializes the dataset and renames columns to match the UI requirements."""
    try:
        print("🚀 Initializing Neural Engine... Please wait.")
        # index_col=0 handles the leading comma often found in Books.csv exports
        df = pd.read_csv('data/Books.csv', index_col=0)
        
        # Mapping CSV headers to the lowercase names used in your Jinja2 templates
        df = df.rename(columns={
            'Title': 'title',
            'Author': 'author',
            'Image-URL': 'image',
            'Publication Year': 'year'
        })

        # Fill missing values to prevent frontend crashes
        df['title'] = df['title'].fillna('Unknown Title')
        df['author'] = df['author'].fillna('Unknown Author')
        
        # Combine features for the TF-IDF Vectorizer
        df['features'] = df['title'].str.lower() + " " + df['author'].str.lower()
        
        print(f"✅ {len(df)} Books Loaded Successfully.")
        return df
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        # Return an empty dataframe with expected columns if loading fails
        return pd.DataFrame(columns=['title', 'author', 'image', 'year', 'features'])

data = initialize_engine()

# Global variables for the Recommender math logic
if not data.empty:
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['features'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
else:
    tfidf_matrix = None
    cosine_sim = None

# --- 🏗️ HELPER FUNCTIONS ---

def get_recommendations(book_title, n=10):
    """Finds similar books using the Cosine Similarity matrix."""
    try:
        # Match title case-insensitively
        idx = data[data['title'].str.lower() == book_title.lower()].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_indices = [i[0] for i in sim_scores[1:n+1]]
        return data.iloc[top_indices]
    except (IndexError, KeyError):
        # Fallback to random samples if the book isn't found
        return data.sample(n)

def format_for_ui(df):
    """Converts dataframe rows to dictionaries for the HTML grid rendering."""
    return [
        {
            "title": row['title'],
            "author": row['author'],
            "image": row['image'] if str(row['image']) != 'nan' else 'https://via.placeholder.com/150',
            "year": row['year'],
            "rating": round(random.uniform(4.0, 4.9), 1)
        }
        for _, row in df.iterrows()
    ]

# --- 🏠 ROUTES ---

@app.route('/')
def home():
    # Selecting books for the different sections of your template
    trending = format_for_ui(data.sample(12))
    popular = format_for_ui(data.sample(8))
    arrivals = format_for_ui(data.sort_values(by='year', ascending=False).head(10))
    
    return render_template("index.html", user=None, user=None, 
                           trending=trending, 
                           popular=popular, 
                           arrivals=arrivals, user=None)

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint for the Doodle AI Chat interface."""
    user_input = request.json.get("message", "").strip().lower()
    
    if "recommend" in user_input or "book" in user_input:
        # Recommending based on a random sample to simulate "AI discovery"
        sample_recs = get_recommendations(data.iloc[random.randint(0, 100)]['title'])
        reply = "<b>Doodle AI Analysis:</b> You might like these books based on their content vectors:<br><br>"
        for _, row in sample_recs.head(3).iterrows():
            reply += f"📚 {row['title']} by {row['author']}<br>"
        return jsonify({"reply": reply})

    return jsonify({"reply": "I am Doodle AI. Ask me for a book recommendation!"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Placeholder for user login logic."""
    # In a full implementation, you would verify credentials here
    session['user'] = "Guest"
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    """Clears the session and redirects back to the home page."""
    session.clear()
    return redirect(url_for('home'))

# --- 🚀 SERVER START ---
if __name__ == "__main__":
    # Ensure the app runs in debug mode for development
    app.run(debug=True, port=8000)