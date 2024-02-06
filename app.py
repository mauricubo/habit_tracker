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
        #tlsInsecure=eval(os.environ.get("INSECURE_SSL")),
    )

    DB_NAME = os.environ.get("DB_NAME")
    
    app.db = client[DB_NAME]
    if DB_NAME not in client.list_database_names():
        app.db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
        print("Created db '{}' with shared throughput.\n".format(DB_NAME))
    else:
        print("Using database: '{}'.\n".format(DB_NAME))

    app.register_blueprint(pages)
    return app

