from cleantext import clean
from nlp import Digester, WordToVec

class Purificator:
    __instance__ = None

    def __init__(self):
        self.digesting = Digester.get_instance()
        self.word2vec = WordToVec.get_instance()
        if Purificator.__instance__ is None:
            Purificator.__instance__ = self
        else:
            raise Exception("You can not create another Purificator class. Use Purificator.get_instance() instead.")

    @staticmethod
    def get_instance():
        """
        Static method to fetch the current instance.
        """
        if not Purificator.__instance__:
            Purificator()
        return Purificator.__instance__

    def text_cleaner(self, text_body: str)-> str:
        return clean(
            text=text_body,
            no_punct=True,
            no_numbers=True,
            no_currency_symbols=True,
            no_urls=True,
            replace_with_punct="",
            replace_with_number="",
            replace_with_currency_symbol="",
            replace_with_url="")

    def stop_word_cleaner(self, text_body: str)-> list:
        return [word for word in text_body.split(" ") if word not in self.digesting.en_stop_words]

    def non_vocab_cleaner(self, words: list)-> list:
        return [word for word in words if self.word2vec.word_in_vocab(word)]
