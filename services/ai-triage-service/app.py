from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
from nltk.corpus import stopwords

app = Flask(__name__)
CORS(app) # Allow requests from any origin for simplicity

# --- Load the Trained Model ---
# The model is loaded only once when the server starts.
try:
    model = joblib.load('symptom_classifier.pkl')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: Model file 'symptom_classifier.pkl' not found.")
    print("Please run the train.py script first to generate the model.")
    model = None
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    model = None

# --- Text Preprocessing Function (Must be IDENTICAL to the one in train.py) ---
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

# --- API Route for Prediction ---
@app.route('/api/predict', methods=['POST'])
def predict_department():
    if model is None:
        return jsonify({"error": "Model is not loaded. Cannot make predictions."}), 500
        
    data = request.get_json()
    
    if not data or 'symptoms' not in data:
        return jsonify({"error": "Invalid input. 'symptoms' key is required."}), 400

    symptoms = data['symptoms']
    
    # Preprocess the input symptoms
    processed_symptoms = preprocess_text(symptoms)
    
    # Make a prediction using the loaded model
    # The model expects a list of texts, so we put our text in a list
    prediction = model.predict([processed_symptoms])
    
    # The prediction is an array, so we get the first (and only) item
    recommended_department = prediction[0]
    
    return jsonify({"recommended_department": recommended_department})

# --- Run the Server ---
if __name__ == '__main__':
    # Run on a different port to avoid conflict with the identity service
    app.run(debug=True, port=5002)