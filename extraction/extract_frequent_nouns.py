import json
import numpy as np
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

INFILE = "../tagging/posts_ner_tagged.json"
OUTFILE = "extracted_entities.json"
TAGS = ["DT", "PP", "JJ", "NN", "NNP"]
THRESHOLD = 8

porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()

#If true use porter stemmer
#If false use wordnet lemmatizer
stemming_flag = False

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		posts = json.load(inf)
		noun_phrases = []
		for post in posts:
			for noun_phrase in post["noun_phrases"]:
				# (NP a/DT massive/JJ big/JJ thank/NN)
				# a massive big thank
				temp = noun_phrase[4:-1]
				temp = temp.split()
				temp = [x.split("/") for x in temp]

				temp2 = []
				for array in filter(lambda x: not("DT" in x or "JJ" in x), temp):
					for string in array:
						if string not in TAGS:
							if stemming_flag:
								if len(string) > 3:
									# Can only stem words that are at least 3 characters long
									temp2.append(porter_stemmer.stem(string))
							else:
								temp2.append(wordnet_lemmatizer.lemmatize(string))

				temp = " ".join(temp2)
				if len(temp) < 2 or temp.isspace():
					# Discard single characters and whitespace
					continue
				noun_phrases.append(temp.lower())

		frequent_nouns = dict()
		for noun_phrase in noun_phrases:
			if noun_phrase not in frequent_nouns:
				frequent_nouns[noun_phrase] = 0

			frequent_nouns[noun_phrase] += 1

		frequent_nouns = {k: v for k, v in frequent_nouns.iteritems() if v >= THRESHOLD}
		frequent_nouns = sorted(frequent_nouns.keys())

		print("All noun phrases: {}".format(len(noun_phrases)))
		print("Noun phrases with frequency >= {}: {}".format(THRESHOLD, len(frequent_nouns)))

		json.dump(frequent_nouns, outf, indent=2)