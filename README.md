# Aspect Based Entity Analysis (ABSA)



## Overview
```
├── data  # The Data and Preprocessing Scripts
│   ├── data_parser.py
│   ├── data_preprocess.py
│   ├── posts.json
│   ├── posts_preprocessed.json
│   └── Tesco
├── extraction  # Scripts for Entitiy and Aspect Extraction
│   ├── extract_entities.py
│   ├── find_aspects.py
│   ├── products_and_aspects.json
│   └── products.json
├── Final Product  # Final Report
├── lexicon_analysis  # Sentiment Analysis and Baseline
│   ├── aggregated_opinions.json
│   ├── aggregate_opinions.py
│   ├── test_accuracy.py
│   ├── testing_posts.json
│   ├── testing_posts_labeled.json
│   ├── testing_posts_vader.json
│   ├── test_posts_1.json
│   ├── test_posts_2.json
│   ├── test_posts_3.json
│   └── test_posts_4.json
├── Project Plan  # Initial Report
├── README.md 
├── Related Articles  # Research Material and Further Reading
├── tagging  # POS Tagging R Scripts
│   ├── complete_tagged_coref.json
│   ├── complete_tagged.json
│   ├── pos_tagged_coref.json
│   ├── pos_tagged.json
│   ├── r_tagger_coref.R
│   └── r_tagger.R
└── visualization  # Visualization through a Local Webserver
    ├── data
    │   ├── aggregated_opinions.json
    │   └── sentimentwords.json
    ├── server.py
    ├── static
    │   ├── app.js
    │   └── style.css
    └── templates
        ├── data.html
        └── index.html
```

## Setting up Python
Set up a Python3.6 virtual environment and install the supplied requirements.

- Create Virtual Environment `virtualenv -p python3.6 venv`
- Activate it `source venv/bin/activate`
- Install dependencies `python3.6 -m pip install -r requirements.txt`

## Setting up R
Set up R on your operating system, for Ubuntu:

- Install R `sudo apt-get install r-base r-base-dev`
- Install Dependencies `sudo R`, then interactively
    - `install.packages(c("rjson","dplyr","NLP","openNLP","jsonlite","stringr","dplyr"))`
    - `install.packages("openNLPmodels.en", repos = "http://datacube.wu.ac.at/", type = "source")`

Alternatively use [R-Studio](https://www.rstudio.com/) and comment in the first lines to install dependencies.

## Recreate Project Results

- Preprocessing
    - Execute `python3.6 data/data_parser.py` to generate `posts.json` from `data/Tesco/`
    - Execute `python3.6 data/data_preprocess.py` to generate `posts_preprocessed.json` from `posts.json`
        - Removes posts with images and less then 20 characters
- POS Tagging
    - Execute `R < tagging/r_tagger.R --no-save` to generate `complete_tagged.json`
        - Uses OpenNLP to add Port of Speech (POS) tags
- Aspect and Entity Extraction
    - Execute `python3.6 extraction/extract_entities.py` to generate `products.json`
    - Execute `python3.6 extraction/find_aspects.py` to generate `products_and_aspects.json`
- Visualization
    - Execute `python3.6 visualization/server.py` and browse to `http://localhost:5000`