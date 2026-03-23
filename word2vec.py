from processamento import main
import numpy as np
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.naive_bayes import GaussianNB

def word2vec():
    df = main()

    # treinar Word2Vec
    model_w2v = Word2Vec(
        sentences=df["tokens"],
        vector_size=100,
        window=5,
        min_count=2,
        workers=4
    )

    # função para vetorizar um documento
    def document_vector(tokens):
        vectors = [model_w2v.wv[word] for word in tokens if word in model_w2v.wv]

        if len(vectors) == 0:
            return np.zeros(model_w2v.vector_size)

        return np.mean(vectors, axis=0)

    # transformar todos os tweets em vetores
    X_w2v = np.array(df["tokens"].apply(document_vector).tolist())
    print("Word2Vec shape:", X_w2v.shape)

    # split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X_w2v, df["sentiment"], test_size=0.2, random_state=42
    )

    # classificador
    model = GaussianNB()
    model.fit(X_train, y_train)

    # previsões
    y_pred = model.predict(X_test)

    # métricas
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")

    print(f"Accuracy: {acc:.4f}")
    print(f"F1: {f1:.4f}")

    return acc, f1

if __name__ == "__main__":
    word2vec()

'''
Word2Vec shape: (1500, 100)
Accuracy: 0.5267
F1: 0.5114
'''