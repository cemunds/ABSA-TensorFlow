from flask import Flask, jsonify, render_template
from flask_cors import cross_origin
import json
app = Flask(__name__)

SENTWORDSFILE = "data/sentimentwords.json"
DATAFILE = "data/aggregated_opinions.json"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/visualizations")
def visualizations():
	return render_template("visualizations.html", data=None)

@app.route("/data", methods=["GET"])
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

if __name__ == '__main__':
	app.run()