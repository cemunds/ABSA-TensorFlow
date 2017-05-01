import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

INFILE = "posts_marked_sentiment_words.json"
OUTFILE = "posts_applied_sentiment_shifters.json"

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		posts = json.load(inf)
		for idx, post in enumerate(posts):
			#post["post_applied_sentiment_shifters"] = []	
			#print(post["post_message_marked_sentiment_words"])

			#for sentence in post["post_message_marked_sentiment_words"]:
				#print("Processed sentence {}".format(sentence))
				#shifter = false
			sentences = nltk.sent_tokenize(post["post_message"].encode("ascii", "ignore"))

			for sentence in sentences:
				print sentence
				ss = sia.polarity_scores(sentence)
				for k in ss:
					print('{0}: {1}, '.format(k, ss[k], end=''))
				print()

				

			

				
