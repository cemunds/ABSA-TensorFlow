import json
import nltk

INFILE = "extracted_entities_cleaned.json"
OUTFILE = "entities_with_aspects.json"

dictionary = dict()

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		entities = json.load(inf)
		for idx, entity in enumerate(entities):
			dictionary[entity] = ["general"]
			# TODO: Find other aspects
			print("Processed entity {}".format(idx))
		json.dump(dictionary, outf, indent=2)