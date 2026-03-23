from processamento import main

from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression


def bert():
    df = main()

    print("\nA gerar embeddings com BERT...")

    model_name = "neuralmind/bert-base-portuguese-cased"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    bert_model = AutoModel.from_pretrained(model_name)

    def bert_embedding(text):

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        with torch.no_grad():
            outputs = bert_model(**inputs)

        embedding = outputs.last_hidden_state[:,0,:]

        return embedding.squeeze().numpy()


    df["bert_vector"] = df["tweet"].apply(bert_embedding)


    X_bert = np.vstack(df["bert_vector"].values)

        # dividir dados
    X_train, X_test, y_train, y_test = train_test_split(
        X_bert, df["sentiment"], test_size=0.2, random_state=42
        )

    # modelo simples de classificação
    clf = LogisticRegression(max_iter=1000)

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    bert_acc = accuracy_score(y_test, y_pred)
    bert_f1 = f1_score(y_test, y_pred, average="weighted")

    print("\nResultados BERT")
    print("Accuracy:", bert_acc)
    print("F1:", bert_f1)

    return bert_acc, bert_f1