import pandas as pd
import pickle
import scipy.sparse as sp

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv('fake_job_postings.csv')

# -------------------------------
# 🔹 Combine multiple text columns
# -------------------------------
df['combined_text'] = (
    df['title'].fillna('') + ' ' +
    df['company_profile'].fillna('') + ' ' +
    df['description'].fillna('') + ' ' +
    df['requirements'].fillna('')
)

# -------------------------------
# 🔹 Structured features
# -------------------------------
df['has_profile'] = df['company_profile'].notnull().astype(int)
df['has_requirements'] = df['requirements'].notnull().astype(int)
df['desc_length'] = df['description'].apply(lambda x: len(str(x)))

# -------------------------------
# 🔹 Rule-based feature
# -------------------------------
suspicious_words = ['earn money fast', 'no experience', 'whatsapp', 'telegram']

def rule_score(text):
    text = str(text).lower()
    return sum(word in text for word in suspicious_words)

df['rule_score'] = df['combined_text'].apply(rule_score)

# -------------------------------
# 🔹 TF-IDF vectorization
# -------------------------------
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    stop_words='english'
)

X_text = vectorizer.fit_transform(df['combined_text'])

# -------------------------------
# 🔹 Combine all features
# -------------------------------
X_struct = df[['has_profile', 'has_requirements', 'desc_length', 'rule_score']].values

X_final = sp.hstack((X_text, X_struct))

y = df['fraudulent']

# -------------------------------
# 🔹 Train model
# -------------------------------
model = LogisticRegression(class_weight='balanced')
model.fit(X_final, y)

# -------------------------------
# 🔹 Save model & vectorizer
# -------------------------------
pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))

print("✅ Model trained successfully!")