# system imports
import multiprocessing
from math import ceil

# API runner imports
from api import create_app
from api_runner import MyCustomApplication

# disable GENSIM package warnings
import warnings
warnings.filterwarnings(action='ignore',category=UserWarning,module='gensim')
warnings.filterwarnings(action='ignore',category=FutureWarning,module='gensim')

# local imports
import settings
from scraper import Crawler
from nlp import Digester, WordToVec, Purificator

def number_of_workers():
    return ceil(multiprocessing.cpu_count() / 2)

if __name__ == "__main__":
    # create important Scrapper and NLP instances
    crawling = Crawler.get_instance()
    digesting = Digester.get_instance()
    purify = Purificator.get_instance()
    word2vec = WordToVec.get_instance()

    options = {
        "bind": '%s:%s' % (f"{settings.HOST}", f"{settings.PORT}"),
        'workers': number_of_workers(),
        "timeout": settings.W_TIMEOUT
    }
    with open('driver.ini') as file:
        line = file.readlines()
        DRIVER_PATH = eval(line[0].split('=')[1])
        file.close()
    MyCustomApplication(create_app(crawling, digesting, purify, word2vec, DRIVER_PATH), options).run()
