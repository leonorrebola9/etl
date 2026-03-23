import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def main():
    # downloads necessários
    nltk.download('punkt')
    nltk.download('punkt_tab')
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

    return df