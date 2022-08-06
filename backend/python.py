import os
import json
from flask import Flask, jsonify, request, redirect
from yt_dlp import YoutubeDL
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import datetime
import requests

from functions.handler_json import handler_json, handler_json_file, handler_downloader
from functions.downloader import download

load_dotenv('.env')
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db' : 'ytdlp',
    'host' : os.environ.get('MONGODB_SERVER'),
    'port':  27017,
    'username' : os.environ.get("MONGODB_USER"),
    'password' : os.environ.get("MONGODB_PASSWORD"),
    'authentication_source' : 'admin'
}

from classes.shared import mongo_db

mongo_db.init_app(app)

# Blueprints
from blueprints.mongo import mongo_bp

app.register_blueprint(mongo_bp)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def default_route():
    return('Default')

if __name__ == "__main__":
    app.run(host='0.0.0.0')