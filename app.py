import os
import ssl
from flask import Flask
from routes import pages
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    client = MongoClient(
        os.environ.get("MONGODB_URI"),
    )

    DB_NAME = os.environ.get("DB_NAME")
    app.db = client[DB_NAME]

    app.register_blueprint(pages)
    return app

