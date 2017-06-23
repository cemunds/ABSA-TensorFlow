import json
import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tqdm import tqdm

def get_sentiment_vector(polarity_scores):
	result = []
	result.append(polarity_scores["neg"])
	result.append(polarity_scores["neu"])
	result.append(polarity_scores["pos"])
	result.append(polarity_scores["compound"])
	return np.array(result)

def calculate_sentiment_score(sentence_sentiment, post_sentiment):
	sentence_argmax = np.argmax(sentence_sentiment[:3])
	post_argmax = np.argmax(post_sentiment[:3])

	if sentence_argmax == 2 or sentence_sentiment[3] > 0.3:
		return 1
	elif sentence_argmax == 0 or sentence_sentiment[3] < -0.3:
		return -1
	else:
		return 0

def aggregate(posts, products, excerpts):
	triples = []
	for post in posts:
		triples += post["sentiments"]
	result = []

	for product, aspects in tqdm(products.items()):
		temp = {}
		temp["name"] = product
		temp["aspects"] = []
		for aspect in aspects:
			negative_score = 0
			neutral_score = 0
			positive_score = 0
			for triple in triples:
				if triple[0] == product and triple[1] == aspect:
					if triple[2] == "negative":
						negative_score += 1
					elif triple[2] == "positive":
						positive_score += 1
					elif triple[2] == "neutral":
						neutral_score += 1

			if negative_score == 0 and neutral_score == 0 and positive_score == 0:
				continue

			temp["aspects"].append({
				"name": aspect,
				"sentiments": [
					{
						"label": "negative",
						"value": negative_score
					},
					{
						"label": "neutral",
						"value": neutral_score
					},
					{
						"label": "positive",
						"value": positive_score
					}
				],
				"posts": excerpts[(product, aspect)] if (product, aspect) in excerpts else []
			})
		result.append(temp)
	return result

def extract_triples(post, products, sentiment_analyzer):
	post_message = post["post_message"].lower()
	post_sentiment = get_sentiment_vector(sentiment_analyzer.polarity_scores(post["post_message"]))
	post["sentiments"] = []
	excerpts = []
	for product, aspects in products.items():
		if product.lower() not in post_message:
			continue

		sentences = nltk.sent_tokenize(post_message)
		sentences_original_casing = nltk.sent_tokenize(post["post_message"])
		for i, sentence in enumerate(sentences):
			if product.lower() not in sentence:
				continue

			sentence_sentiment = get_sentiment_vector(sentiment_analyzer.polarity_scores(sentence))
			score = calculate_sentiment_score(sentence_sentiment, post_sentiment)

			if score <= -1:
				polarity = "negative"
			elif score >= 1:
				polarity = "positive"
			else:
				polarity = "neutral"

			aspect_found = False
			for aspect in aspects:
				if aspect.lower() not in sentence:
					continue

				post["sentiments"].append((product, aspect, polarity))
				excerpts.append((product, aspect, sentences_original_casing[i]))
				aspect_found = True

			if not aspect_found:
				post["sentiments"].append((product, "general", polarity))
				excerpts.append((product, "general", sentences_original_casing[i]))

	return post, excerpts

if __name__ == "__main__":

	INFILE = "../tagging/complete_tagged.json"
	OUTFILE = "posts_sentiment_triples.json"
	AGROUTFILE = "aggregated_opinions.json"
	PRODUCTSFILE = "../extraction/products_and_aspects.json"

	sid = SentimentIntensityAnalyzer()

	with open(PRODUCTSFILE, "r") as prodf:
		products = json.load(prodf)

	with open(INFILE, "r") as inf:
		posts = json.load(inf)

	post_results = []
	all_excerpts = []
	for post in tqdm(posts):
		result_post, excerpts = extract_triples(post, products, sid)
		post_results.append(result_post)
		all_excerpts += excerpts

	temp = {}
	for product, aspect, sentence in all_excerpts:
		if (product, aspect) not in temp:
			temp[(product, aspect)] = []

		if len(temp[(product, aspect)]) < 10:
			temp[(product, aspect)].append(sentence)

	aggregated_result = aggregate(post_results, products, temp)

	with open(OUTFILE, "w") as outf:
		json.dump(post_results, outf, indent=2)

	with open(AGROUTFILE, "w") as agroutf:
		json.dump(aggregated_result, agroutf, indent=2)