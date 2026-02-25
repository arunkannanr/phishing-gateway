import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from feature_extractor import preprocess_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets', 'sms_phising.csv')

def train_gateway_model():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset missing at {DATASET_PATH}")

    # 1. Load your specific CSV
    df = pd.read_csv(DATASET_PATH, encoding='latin-1')
    
    # 2. Cleanup columns (keeping v1 as label, v2 as text)
    df = df[['v1', 'v2']].copy()
    df.columns = ['label', 'message']
    
    # 3. Process and Map
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    df['message'] = df['message'].apply(preprocess_text)

    # 4. Vectorization
    vectorizer = TfidfVectorizer(max_features=3000)
    X = vectorizer.fit_transform(df['message'])
    y = df['label']

    # 5. Train
    model = MultinomialNB()
    model.fit(X, y)

    # 6. Save Connection Files
    joblib.dump(model, os.path.join(BASE_DIR, 'models', 'gateway_model.pkl'))
    joblib.dump(vectorizer, os.path.join(BASE_DIR, 'models', 'vectorizer.pkl'))
    print("✅ Gateway Brain (ML) synchronized and saved.")

if __name__ == "__main__":
    train_gateway_model()