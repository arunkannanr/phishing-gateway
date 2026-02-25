import pandas as pd
import joblib
import os
from sklearn.metrics import accuracy_score

# 1. FIXING THE PATHS
# This points to the folder evaluate.py is currently in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, 'models', 'gateway_model.pkl')
VEC_PATH = os.path.join(BASE_DIR, 'models', 'vectorizer.pkl')

# MATCHING YOUR TYPO: 'sms_phising.csv' (No 'h')
DATASET_PATH = os.path.join(BASE_DIR, 'datasets', 'sms_phising.csv')

def get_accuracy():
    try:
        # 2. LOAD ASSETS
        if not os.path.exists(MODEL_PATH):
            print(f"❌ Cannot find model at: {MODEL_PATH}")
            return
            
        model = joblib.load(MODEL_PATH)
        vec = joblib.load(VEC_PATH)

        # 3. LOAD DATASET
        if not os.path.exists(DATASET_PATH):
            print(f"❌ Cannot find dataset at: {DATASET_PATH}")
            print("Check your 'datasets' folder for the file!")
            return

        # Using latin-1 encoding common for this SMS dataset
        df = pd.read_csv(DATASET_PATH, encoding='latin-1')
        
        # Standardizing columns (v1 = label, v2 = message)
        df = df[['v1', 'v2']]
        df.columns = ['label', 'message']
        df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})

        # 4. PREDICT
        X_test = vec.transform(df['message'])
        y_true = df['label_num']
        y_pred = model.predict(X_test)

        # 5. OUTPUT
        accuracy = accuracy_score(y_true, y_pred)
        print("\n" + "⭐" * 30)
        print(f" SUCCESS! AI ACCURACY: {accuracy * 100:.2f}%")
        print("⭐" * 30)

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    get_accuracy()