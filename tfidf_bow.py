from processamento import main
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score

def tfidf_bow():
    df = main()

    # Bag of Words
    vectorizer_bow = CountVectorizer()
    X_bow = vectorizer_bow.fit_transform(df["texto_limpo"])

    print("BoW vocab:", len(vectorizer_bow.vocabulary_))
    print("BoW shape:", X_bow.shape)

    # TF-IDF
    vectorizer_tfidf = TfidfVectorizer()
    X_tfidf = vectorizer_tfidf.fit_transform(df["texto_limpo"])

    print("TF-IDF shape:", X_tfidf.shape)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        df["texto_limpo"], df["sentiment"], test_size=0.2, random_state=42
    )

    # Pipeline com TF-IDF + Naive Bayes
    model = Pipeline([
        ("vectorizer", TfidfVectorizer()),
        ("classifier", MultinomialNB())
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # métricas
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")

    print(f"Accuracy: {acc:.4f}")
    print(f"F1: {f1:.4f}")

    return acc, f1


if __name__ == "__main__":
    tfidf_bow()

'''
BoW vocab: 4941
BoW shape: (1500, 4941)
TF-IDF shape: (1500, 4941)
Accuracy: 0.7167
F1: 0.7165
'''