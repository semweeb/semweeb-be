from flask import Flask, request
from flask_api import status
from flask_cors import CORS

import json
import sparql

app = Flask(__name__)

CORS(app) # This will enable CORS for all routes

@app.route("/search", methods=["GET"])
def search():
    args = request.args
    query = args.get("q")

    if not query:
        return "Search query not specified.", status.HTTP_400_BAD_REQUEST
    try:
        return sparql.search(query)
    except:
        return "An error occurred while fetching your search results.", status.HTTP_500_BAD_REQUEST

@app.route("/suggestions", methods=["GET"])
def suggestions():
    args = request.args
    query = args.get("q")

    if not query:
        return json.dumps([])

    try:
        return sparql.get_suggestions(query)
    except:
        return "An erro occurred while fetching your search results.", status.HTTP_500_BAD_REQUEST
