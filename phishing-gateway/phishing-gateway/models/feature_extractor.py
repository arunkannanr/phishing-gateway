import re
import string

def preprocess_text(text):
    """
    Standardizes text for the Machine Learning model.
    """
    text = str(text).lower()
    # Remove URLs (often dynamic in phishing)
    text = re.sub(r'http\S+|www\S+|https\S+', 'url_link', text, flags=re.MULTILINE)
    # Remove punctuation and special characters
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove extra whitespace
    text = " ".join(text.split())
    return text