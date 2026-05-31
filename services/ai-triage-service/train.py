import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib # A library to save our trained model
import nltk
from nltk.corpus import stopwords
import re

# --- Download necessary NLTK data ---
# This only needs to be run once.
try:
    stopwords.words('english')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords')
    print("Download complete.")

# --- Text Preprocessing Function ---
def preprocess_text(text):
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    text = text.lower()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

# --- Model Training ---
def train_model():
    print("Starting model training...")
    
    # 1. Load the dataset
    data = pd.read_csv('symptoms_data.csv')
    
    # Check if the required columns exist
    if 'symptom_text' not in data.columns or 'department' not in data.columns:
        raise ValueError("CSV must contain 'symptom_text' and 'department' columns.")
        
    # Apply preprocessing to the symptom text
    data['symptom_text_processed'] = data['symptom_text'].apply(preprocess_text)

    X = data['symptom_text_processed']
    y = data['department']

    # 2. Create a model pipeline
    # This pipeline does two things:
    # a) TfidfVectorizer: Converts text into numerical vectors.
    # b) MultinomialNB: A Naive Bayes classifier suitable for text.
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

    # 3. Train the model
    model_pipeline.fit(X, y)

    # 4. Save the trained model to a file
    joblib.dump(model_pipeline, 'symptom_classifier.pkl')
    
    print("Model training complete. Model saved to 'symptom_classifier.pkl'")

# This part allows us to run the script directly from the command line
if __name__ == '__main__':
    train_model()