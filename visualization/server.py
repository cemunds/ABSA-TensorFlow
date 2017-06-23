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
	data = [
		{
			"name": "iPhone",
			"aspects": [
				{
					"name": "battery",
					"negative": 5,
					"positive": 2,
					"neutral": 3,
					"posts": ["[...] the battery does not last long enough [...]"]
				}
			]
		}
	]
	return render_template("visualizations.html", data=jsonify(data))  # TODO: passing data does not work

@app.route("/data")
def data():
	return render_template("data.html")

@app.route("/get_data", methods=["GET"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def get_data():
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