import gensim
from gensim.summarization import keywords, textcleaner
from nltk.corpus import stopwords

class Gensim:
    def preprocess(self, sentence: str):
        en_stop_words = stopwords.words('english')
        return [word for word in sentence.lower().split() if word not in en_stop_words]
    
    def summarizer(self, text_body: str, briefing: bool):
        if briefing:
            brief_list = self.preprocess(text_body)
            return keywords(text=' '.join(brief_list), words=10, scores=True, lemmatize=True, split=True)
        else:
            return keywords(text=text_body, words=10, scores=True, lemmatize=True, split=True)