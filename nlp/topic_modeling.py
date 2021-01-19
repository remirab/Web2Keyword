import gensim
import gensim.downloader as api
from gensim.summarization import keywords, textcleaner
from gensim import corpora
from gensim.models import Word2Vec
from gensim.similarities.index import AnnoyIndexer
from gensim.models.word2vec import Text8Corpus
from collections import defaultdict
from nltk.corpus import stopwords

class Briefing:
    __instance__ = None

    def __init__(self):
        """
        Constructor
        """
        self.en_stop_words = stopwords.words('english')
        if Briefing.__instance__ is None:
            Briefing.__instance__ = self
        else:
            raise Exception("You can not create another Briefing class. Use Briefing.get_instance() instead.")

    @staticmethod
    def get_instance():
        """
        Static method to fetch the current instance.
        """
        if not Briefing.__instance__:
            Briefing()
        return Briefing.__instance__

    def preprocess(self, sentence: str):
        en_stop_words = self.en_stop_words
        return [word for word in sentence.lower().split() if word not in en_stop_words]
    
    def summarizer(self, text_body: str, remove_stop_words: bool, n_words: int=10):
        if remove_stop_words:
            without_stop_words = self.preprocess(text_body)
            return keywords(text=' '.join(without_stop_words), words=n_words, scores=True, lemmatize=True, split=True)
        else:
            return keywords(text=text_body, words=n_words, scores=True, lemmatize=False, split=True)

class FastSimQuery:
    __instance__ = None

    def __init__(self):
        """
        Constructor
        """
        self.text8_path = api.load('text8', return_path=True)
        self.text8_model = Word2Vec(Text8Corpus(self.text8_path))
        self.annoy_index = AnnoyIndexer(model=self.text8_model, num_trees=100)
        if FastSimQuery.__instance__ is None:
            FastSimQuery.__instance__ = self
        else:
            raise Exception("You can not create another FastSimQuery class. Use FastSimQuery.get_instance() instead.")

    @staticmethod
    def get_instance():
        """
        Static method to fetch the current instance.
        """
        if not FastSimQuery.__instance__:
            FastSimQuery()
        return FastSimQuery.__instance__

    def processor(self, word_vec: str, annoy_indexer: bool):
        if annoy_indexer:
            return self.__approximate_neighbors(word_vec, self.text8_model.wv, self.annoy_index)
        else:
            return self.__normal_neighbors(word_vec, self.text8_model.wv)
    
    def __approximate_neighbors(self, word_vec: str, wv, annoy_index, topn: int=11):
        return wv.most_similar([word_vec], topn=topn, indexer=annoy_index)

    def __normal_neighbors(self, word_vec: str, wv, topn: int=10):
        return wv.most_similar([word_vec], topn=topn)

    def word_in_vocab(self, word: str)-> bool:
        return word in self.text8_model.wv.vocab

class WordToVec:
    __instance__ = None

    def __init__(self):
        """
        Constructor
        """
        self.word2vec_model = api.load('word2vec-google-news-300')
        if WordToVec.__instance__ is None:
            WordToVec.__instance__ = self
        else:
            raise Exception("You can not create another WordToVec class. Use WordToVec.get_instance() instead.")

    @staticmethod
    def get_instance():
        """
        Static method to fetch the current instance.
        """
        if not WordToVec.__instance__:
            WordToVec()
        return WordToVec.__instance__

    def similarity(self, *words)-> float:
        return self.word2vec_model.similarity(words[0], words[1])

    def most_similar(self, positive: list, negative: list, topn: int=5):
        return self.word2vec_model.most_similar(positive=positive, negative=negative, topn=topn)

    def word_in_vocab(self, word: str)-> bool:
        return word in self.word2vec_model.wv.vocab
