import gensim
import gensim.downloader as api
from gensim.summarization import keywords, textcleaner
from gensim import corpora
from gensim.models import Word2Vec, KeyedVectors
from gensim.similarities.index import AnnoyIndexer
from gensim.models.word2vec import Text8Corpus
from collections import defaultdict
from nltk.corpus import stopwords

class Gensim:
    def preprocess(self, sentence: str):
        en_stop_words = stopwords.words('english')
        return [word for word in sentence.lower().split() if word not in en_stop_words]
    
    def summarizer(self, text_body: str, remove_stop_words: bool, n_words: int=10):
        if remove_stop_words:
            without_stop_words = self.preprocess(text_body)
            return keywords(text=' '.join(without_stop_words), words=n_words, scores=True, lemmatize=True, split=True)
        else:
            return keywords(text=text_body, words=n_words, scores=True, lemmatize=False, split=True)
    
    # def dictionarizer(self):
    #     textcleaner.
    #     pass

class FastSimQuery:
    # PARAMS = {
    #     'alpha': 0.05,
    #     'vector_size': 100,
    #     'window': 5,
    #     'epochs': 5,
    #     'min_count': 5,
    #     'sample': 1e-4,
    #     'sg': 1,
    #     'hs': 0,
    #     'negative': 5,
    # }
    def runner(self, word_vec: str, annoy_indexer: bool):
        text8_model = self.__text8_model()
        annoy_index = self.__annoy_index(text8_model[0])
        if annoy_indexer:
            return self.__approximate_neighbors(word_vec, text8_model[1], annoy_index)
        else:
            return self.__normal_neighbors(word_vec, text8_model[1])

    def __text8_model(self):
        text8_path = api.load('text8', return_path=True)
        text8_model = Word2Vec(Text8Corpus(text8_path))
        return text8_model, text8_model.wv
    
    def __annoy_index(self, text8_model):
        return AnnoyIndexer(text8_model, 100)
    
    def __approximate_neighbors(self, word_vec: str, wv, annoy_index, topn: int=11):
        return wv.most_similar([word_vec], topn=topn, indexer=annoy_index)

    def __normal_neighbors(self, word_vec: str, wv, topn: int=10):
        return wv.most_similar([word_vec], topn=topn)
