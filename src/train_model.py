import pickle
from data_preprocessing import clean_data
from content_based import create_features, compute_similarity
from collaborative import create_user_item_matrix, pearson_similarity

print("🚀 Training Hybrid Recommendation Model...")

# Load data
data = clean_data()

# Content-based
data = create_features(data)
content_similarity = compute_similarity(data)

# Collaborative
matrix = create_user_item_matrix(data)
user_similarity = pearson_similarity(matrix)

# Save models
pickle.dump(data, open('models/data.pkl', 'wb'))
pickle.dump(content_similarity, open('models/content_similarity.pkl', 'wb'))
pickle.dump(matrix, open('models/user_matrix.pkl', 'wb'))
pickle.dump(user_similarity, open('models/user_similarity.pkl', 'wb'))

print("✅ Training Complete.")