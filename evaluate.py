import pickle


def pipe_analyzer(x):
    return x.split("|")


def word2features(sent, i):
    word = sent[i]
    features = []
    features.append(word.lower())
    features.append(word[-2:])
    features.append(word[-3:])
    features.append(word[:2])
    features.append(str(word.istitle()))
    features.append(str(word.isdigit()))
    if i > 0:
        features.append(sent[i - 1].lower())
        features.append(sent[i - 1][-2:])
    else:
        features.append("BOS")
        features.append("BOS")
    if i < len(sent) - 1:
        features.append(sent[i + 1].lower())
        features.append(sent[i + 1][-2:])
    else:
        features.append("EOS")
        features.append("EOS")
    return "|".join(features)


# Modeli yükle
with open("model.pkl", "rb") as f:
    clf, le, vectorizer = pickle.load(f)

# Test cümlesi
cumle = input("Cümle girin: ").split()

features = [word2features(cumle, i) for i in range(len(cumle))]
X = vectorizer.transform(features)
y_pred = clf.predict(X)
labels = le.inverse_transform(y_pred)

print("\n--- Tahmin Sonucu ---")
print(f"{'Kelime':<20} {'CHUNK-OUTER':<15} {'CHUNK-INNER':<15} {'CLAUSE'}")
print("-" * 60)
for kelime, etiket in zip(cumle, labels):
    print(f"{kelime:<20} {etiket:<15} {'_':<15} {'O'}")
