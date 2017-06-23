from flask import Flask, jsonify
from flask.ext.cors import cross_origin
import json
app = Flask(__name__)

SENTWORDSFILE = "data/sentimentwords.json"
DATAFILE = "data/aggregated_opinions.json"

@app.route("/", methods=["GET"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def serve_data():
	with open(SENTWORDSFILE, "r") as sf:
		sentimentwords = json.load(sf)

	with open(DATAFILE, "r") as df:
		data = json.load(df)

	result = {
		"sentimentwords": sentimentwords,
		"products": data
	}

	return jsonify(result)
