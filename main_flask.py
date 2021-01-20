import os
import settings
from flask import Flask, Response
from helpers import Utility, LogLevels

os.environ["FLASK_ENV"] = "development"
os.environ["FLASK_DEBUG"] = "0"

def create_app():
    app = Flask(__name__)

    @app.route("/test", methods=["GET"])
    def test_api():
        Utility.log(LogLevels.DEBUG, "Someone test TopicModeling API")
        return Response("It works!", status=200)
    
    return app

if __name__ == '__main__':
    create_app().run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)