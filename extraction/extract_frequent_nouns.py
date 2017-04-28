import json
import numpy as np

INFILE = "../tagging/posts_ner_tagged.json"
OUTFILE = "extracted_entities.json"
TAGS = ["DT", "PP", "JJ", "NN", "NNP"]
THRESHOLD = 8

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
				for array in temp:
					for string in array:
						if string not in TAGS:
							temp2.append(string)

				temp = " ".join(temp2)
				if len(temp) == 0 or temp.isspace():
					continue
				noun_phrases.append(temp)

		frequent_nouns = dict()
		for noun_phrase in noun_phrases:
			if noun_phrase not in frequent_nouns:
				frequent_nouns[noun_phrase] = 0

			frequent_nouns[noun_phrase] += 1

		frequent_nouns = {k: v for k, v in frequent_nouns.iteritems() if v >= THRESHOLD}

		print("All noun phrases: {}".format(len(noun_phrases)))
		print("Noun phrases with frequency >= {}: {}".format(THRESHOLD, len(frequent_nouns)))

		for noun in frequent_nouns:
			outf.write(noun + "\n")