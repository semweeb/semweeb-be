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
    page = args.get("page")
    genres = args.get("genres")
    genre_list = genres.split(";")
    print(genre_list)

    if not query:
        return "Search query not specified.", status.HTTP_400_BAD_REQUEST
    try:
        return sparql.search(query, int(page) * 32, genre_list)
    except:
        return "An error occurred while fetching your search results.", status.HTTP_500_BAD_REQUEST

@app.route("/suggestions", methods=["GET"])
def suggestions():
    args = request.args
    query = args.get("q")

    if not query:
        return json.dumps([])

    try:
        print("\n\n\nWOIIII\n\n\n")
        print(query)
        return sparql.get_suggestions(query)
    except:
        return "An error occurred while fetching your search results.", status.HTTP_500_BAD_REQUEST

@app.route("/details", methods=["GET"])
def details():
    args = request.args
    query = args.get("id")
    anime_id = query.split("/")[-1]

    if not query:
        return "Search query not specified.", status.HTTP_400_BAD_REQUEST
    try:
        return sparql.get_anime_details(anime_id)
    except:
        return "An error occurred while fetching your search results.", status.HTTP_500_BAD_REQUEST

@app.route("/actor-details", methods=["GET"])
def actor_details():
    args = request.args
    query = args.get("id")
    anime_id = query.split("/")[-1]

    if not query:
        return "Search query not specified.", status.HTTP_400_BAD_REQUEST
    try:
        return sparql.get_anime_voice_actor(anime_id)
    except:
        return "An error occurred while fetching your search results.", status.HTTP_500_BAD_REQUEST