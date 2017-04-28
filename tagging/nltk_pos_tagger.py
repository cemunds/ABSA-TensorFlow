import nltk
import json

INFILE = "../data/posts_preprocessed.json"
OUTFILE = "posts_pos_tagged.json"

results = []

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		posts = json.load(inf)
		for idx, post in enumerate(posts):
			sentences = nltk.sent_tokenize(post["post_message"].encode("ascii", "ignore"))
			words = [nltk.word_tokenize(s) for s in sentences]
			post["post_message_pos_tagged_nltk"] = [nltk.pos_tag(sentence) for sentence in words]
			results.append(post)
			print("Processed post {}".format(idx))
		json.dump(results, outf, indent=2)