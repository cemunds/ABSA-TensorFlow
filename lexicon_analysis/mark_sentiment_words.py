import json
import nltk

INFILE = "../extraction/posts_assigned_entities.json"
OUTFILE = "posts_marked_sentiment_words.json"

NEGATIVE_WORDS_FILE = "negative-words.txt"
POSITIVE_WORDS_FILE = "positive-words.txt"

negative_words = []
positive_words = []

with open(NEGATIVE_WORDS_FILE, "r") as negf:
	negative_words = [x.strip() for x in negf.readlines()]

with open(POSITIVE_WORDS_FILE, "r") as posf:
	positive_words = [x.strip() for x in posf.readlines()]

print("Found {} negative words".format(len(negative_words)))
print("Found {} positive words".format(len(positive_words)))

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		posts = json.load(inf)

		for idx, post in enumerate(posts):
			post["post_message_marked_sentiment_words"] = []
			sentences = nltk.sent_tokenize(post["post_message"].encode("ascii", "ignore"))
			tokens = [nltk.word_tokenize(s) for s in sentences]
			for sentence in tokens:
				temp = []
				for token in sentence:
					if token in negative_words:
						temp.append((token, -1))
					elif token in positive_words:
						temp.append((token, 1))
					else:
						temp.append((token, 0))
				post["post_message_marked_sentiment_words"].append(temp)
			print("Processed post {}".format(idx))
		json.dump(posts, outf, indent=2, separators=(',', ': '))
