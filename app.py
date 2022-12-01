from flask import Flask, request
from flask_api import status

import sparql

app = Flask(__name__)

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


