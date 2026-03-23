import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score


def main():
    nltk.download('punkt')
    nltk.download('stopwords')

    df = pd.read_csv("tweet_sub.csv")

    stop_words = set(stopwords.words('portuguese'))

    def preprocessar(texto):
        texto = texto.lower()
        texto = texto.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(texto)
        tokens = [t for t in tokens if t not in stop_words]
        return tokens

    df["tokens"] = df["tweet"].apply(preprocessar)
    df["texto_limpo"] = df["tokens"].apply(lambda x: " ".join(x))

    return df   # ← devolve o dataframe


if __name__ == "__main__":
    df = main()   # ← agora df existe aqui

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

    # Métricas formatadas
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"F1: {f1_score(y_test, y_pred, average='weighted'):.4f}")