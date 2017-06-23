from flask import Flask, jsonify, render_template, request
from flask_cors import cross_origin
import pandas as pd
from bokeh.charts import Bar
from bokeh.embed import components
import json
app = Flask(__name__)

SENTWORDSFILE = "data/sentimentwords.json"
DATAFILE = "data/aggregated_opinions.json"

def create_figure(feature_name):
	df = pd.DataFrame.from_dict({
		"sentiment": ["Pos", "Neu", "Neg"],
		"value": [0, 1, 5]
	})
	print(df)
	p = Bar(data=df, title="Sentiment", values="value", width=600, height=400)
	p.xaxis.axis_label = "Category"
	p.yaxis.axis_label = "Strength"
	return p

@app.route("/test")
def test():
	feature_names = ["Entity", "Another Entity"]
	current_feature_name = request.args.get("feature_name")
	plot = create_figure(current_feature_name)
	script, div = components(plot)
	return render_template("test.html", script=script, div=div, feature_names=feature_names,  current_feature_name=current_feature_name)

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