import json

INFILE = "extracted_entities.json"
OUTFILE = "extracted_entities_cleaned.json"

BLACKLIST_FILE = "entity_blacklist.json"

with open(BLACKLIST_FILE, "r") as blf:
	entity_blacklist = json.load(blf)

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		entities = json.load(inf)
		json.dump(filter(lambda x: x not in entity_blacklist, entities), outf, indent=2)