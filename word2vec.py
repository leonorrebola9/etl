import pandas as pd
import nltk
import string
import numpy as np

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.naive_bayes import GaussianNB

from gensim.models import Word2Vec

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

    # preprocessing
    df["tokens"] = df["tweet"].apply(preprocessar)

    # WORD2VEC
    model_w2v = Word2Vec(
        sentences=df["tokens"],
        vector_size=100,
        window=5,
        min_count=2,
        workers=4
    )

    # função para vetor de documento
    def document_vector(tokens):
        vectors = []

        for word in tokens:
            if word in model_w2v.wv:
                vectors.append(model_w2v.wv[word])

        if len(vectors) == 0:
            return np.zeros(model_w2v.vector_size)

        return np.mean(vectors, axis=0)

    # transformar tweets em vetores
    X_w2v = np.array(df["tokens"].apply(document_vector).tolist())

    print("Word2Vec shape:", X_w2v.shape)

    # classificação
    X_train, X_test, y_train, y_test = train_test_split(
        X_w2v, df["sentiment"], test_size=0.2, random_state=42
    )

    model = GaussianNB()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(f"F1:", f1_score(y_test, y_pred, average="weighted".:2f))

if __name__ == "__main__":
    main()

'''
Word2Vec shape: (1500, 100)
Accuracy: 0.54
F1: 0.5273828571428572
'''