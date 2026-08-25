import os
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def load_data(filepath):
    sentences = []
    current = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "":
                if current:
                    sentences.append(current)
                    current = []
                continue
            parts = line.split()
            if len(parts) >= 5:
                current.append((parts[1], parts[2], parts[3], parts[4]))
            elif len(parts) >= 3:
                current.append((parts[1], parts[2], "_", "O"))
    if current:
        sentences.append(current)
    return sentences


def word2features(sent, i):
    word = sent[i][0]
    features = []
    features.append(word.lower())
    features.append(word[-2:])
    features.append(word[-3:])
    features.append(word[:2])
    features.append(str(word.istitle()))
    features.append(str(word.isdigit()))
    if i > 0:
        features.append(sent[i - 1][0].lower())
        features.append(sent[i - 1][0][-2:])
    else:
        features.append("BOS")
        features.append("BOS")
    if i < len(sent) - 1:
        features.append(sent[i + 1][0].lower())
        features.append(sent[i + 1][0][-2:])
    else:
        features.append("EOS")
        features.append("EOS")
    return "|".join(features)


sentences = load_data("data/train.conll")
print(f"Toplam cümle: {len(sentences)}")

all_features = []
all_labels = []
for sent in sentences:
    for i in range(len(sent)):
        all_features.append(word2features(sent, i))
        all_labels.append(sent[i][1])

# Feature encoding
from sklearn.feature_extraction.text import HashingVectorizer


def pipe_analyzer(x):
    return x.split("|")


vectorizer = HashingVectorizer(analyzer=pipe_analyzer)
X = vectorizer.transform(all_features)

le = LabelEncoder()
y = le.fit_transform(all_labels)

# Train/test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Kaydet
with open("model.pkl", "wb") as f:
    pickle.dump((clf, le, vectorizer), f)

# Sonuçlar
print("\n--- Sonuçlar ---")
print(
    classification_report(
        y_test, y_pred, labels=list(range(len(le.classes_))), target_names=le.classes_
    )
)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=le.classes_, yticklabels=le.classes_)
plt.title("Confusion Matrix")
plt.ylabel("Gerçek")
plt.xlabel("Tahmin")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()
print("Grafik kaydedildi: confusion_matrix.png")
