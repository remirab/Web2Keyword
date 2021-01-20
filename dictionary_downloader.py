from nltk import download
import gensim.downloader as api

if __name__ == "__main__":
    api.load('word2vec-google-news-300')
    download('stopwords', quiet=True)