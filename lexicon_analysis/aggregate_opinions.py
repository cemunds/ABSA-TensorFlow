import json

"""
Opinions are not yet aggregated properly according to the proposed formula.
This is just a proof of concept.
"""

INFILE = "posts_marked_sentiment_words.json"
OUTFILE = "posts_aggregated_opinions.json"
ENTITIESFILE = "../extraction/entities_with_aspects.json"

with open(ENTITIESFILE, "r") as entf:
	entities = json.load(entf)

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		posts = json.load(inf)
		for idx, post in enumerate(posts):
			sentiments = []
			for sentence in post["post_message_marked_sentiment_words"]:
				mentioned_entities = []
				score = 0

				for token in sentence:
					score += token[1]
					if token[0] in post["entities"]:
						mentioned_entities.append(token[0])

				if score == 0:
					polarity = "neutral"
				elif score > 0:
					polarity = "positive"
				else:
					polarity = "negative"

				for entity in mentioned_entities:
					if entity in entities:
						aspect = entities[entity][0]
					else:
						print("WARNING: Entity '{}' not in list of entities".format(entity))
						aspect = "general"
					sentiments.append((entity, aspect, polarity))

			post["opinons"] = sentiments
			print("Processed post {}".format(idx))
		json.dump(posts, outf, indent=2)