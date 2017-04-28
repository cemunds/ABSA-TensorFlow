import json

INFILE = "../tagging/posts_ner_tagged.json"
OUTFILE = "posts_assigned_entities.json"

ENTITIES_FILE = "extracted_entities_cleaned.json"

with open(ENTITIES_FILE, "r") as enf:
	entities = json.load(enf)

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		posts = json.load(inf)
		for idx, post in enumerate(posts):
			mentioned_entities = set(post["entities"])
			for noun_phrase in post["noun_phrases"]:
				for entity in entities:
					if entity in noun_phrase:
						mentioned_entities.add(entity)
			post["entities"] = list(mentioned_entities)
			print("Processed post {}".format(idx))
		json.dump(posts, outf, indent=2)