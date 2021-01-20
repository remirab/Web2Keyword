import json
import uuid
import settings
import numpy as np
from functools import singledispatch
from flask import Flask, Response, request
from datetime import datetime
from helpers import Utility, LogLevels

@singledispatch
def to_serializable(val):
    """Used by default."""
    return str(val)

@to_serializable.register(np.float32)
def ts_float32(val):
    """Used if *val* is an instance of numpy.float32."""
    return np.float64(val)

@to_serializable.register(datetime)
def ts_datetime(val):
    """Used if *val* is an instance of datetime.datetime."""
    return val.isoformat() + "Z"

def create_app(crawling, digesting, purify, word2vec, DRIVER_PATH):
    app = Flask(__name__)

    @app.route("/query", methods=["POST", "GET"])
    def query():
        Utility.log(LogLevels.DEBUG, "A query request received")
        try:
            input_data = {}
            input_data.update({"url": request.args.get("url")})
            input_data.update({"product_list": eval(request.args.get("product_list"))})
            
            input_data.update({ 'product_list': list(set(word for item in [sentence.split(" ") for sentence in input_data["product_list"]] for word in item)) })
            
            uid = uuid.uuid5(uuid.NAMESPACE_URL, input_data["url"])

            url_contents = crawling.spider(url=input_data["url"], driver_path=DRIVER_PATH)
            url_contents_cleaned = purify.text_cleaner(text_body=url_contents)
            url_contents_cleaned = list(set(purify.stop_word_cleaner(text_body=url_contents_cleaned)))
            filtered_url_contents = purify.non_vocab_cleaner(url_contents_cleaned)
            filtered_product_list = purify.non_vocab_cleaner(input_data["product_list"])
            if len(filtered_product_list) == 0:
                return Response(f"Your input sentences or words was not present in model vocabulary. Please change them.", status=404, content_type="application/json")
            
            result = {}
            for url_word in filtered_url_contents:
                cross_sim = [word2vec.similarity(url_word, input_word) for input_word in filtered_product_list]
                max_cross_sim = max(cross_sim)
                if max_cross_sim > 0.09:
                    result.update({url_word: max_cross_sim})

            payload = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[0:20])
            
            return Response(json.dumps(payload, default=to_serializable), status=200, content_type="application/json")
        except Exception as ex:
            return Response(f"Something goes wrong:\n{str(ex)}", status=500)

    @app.route("/test", methods=["GET"])
    def test_api():
        Utility.log(LogLevels.DEBUG, "Someone test TopicModeling API")
        return Response("It works!", status=200)

    return app
    
