#!/usr/bin/env python3.6
from flask import Flask, render_template
app = Flask(__name__)


def load_dummy():
    return {
        "name": "Sample Product",
        "aspects": [
            {
                "sentiments": [1, 2, 3, 4, 5],
                "posts": [
                    {
                        "data": None,
                        "sentimentwords": "",
                        "product": ""
                    }
                ]
            }

        ]
    }


def load_data():
    pass


def preprocess_data():
    pass


@app.route('/')
def index():
    return render_template("index.html", product=load_dummy())

if __name__ == '__main__':
    app.run(debug=True)