from flask import Flask, jsonify, render_template, request
from flask_cors import cross_origin
import pandas as pd
import json
import os

app = Flask(__name__)
MYDIR = os.path.dirname(__file__)
SENTWORDSFILE =  os.path.join(MYDIR, "data/sentimentwords.json")
DATAFILE = os.path.join(MYDIR,"data/aggregated_opinions.json")

@app.route("/")
def index():
	return render_template("index.html")

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