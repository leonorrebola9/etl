from bert import bert
from processamento import main  
from tfidf_bow import tfidf_bow
from word2vec import word2vec

def graficos():
    acc_bow, f1_bow = tfidf_bow()
    acc_bert, f1_bert = bert()
    acc_w2v, f1_w2v = word2vec()

    import matplotlib.pyplot as plt

    # Gráfico de Accuracy
    plt.figure(figsize=(10, 5))
    plt.bar(["TF-IDF + NB", "BERT", "Word2Vec"], [acc_bow, acc_bert, acc_w2v], color=["blue", "orange", "green"])
    plt.title("Accuracy dos Modelos")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)
    plt.show()

    # Gráfico de F1 Score
    plt.figure(figsize=(10, 5))
    plt.bar(["TF-IDF + NB", "BERT", "Word2Vec"], [f1_bow, f1_bert, f1_w2v], color=["blue", "orange", "green"])
    plt.title("F1 Score dos Modelos")
    plt.ylabel("F1 Score")
    plt.ylim(0, 1)
    plt.show()

if __name__ == "__main__":
    graficos()