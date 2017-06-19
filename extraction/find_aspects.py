import json
import nltk

POSTSFILE = "../tagging/complete_tagged.json"
INFILE = "products.json"
OUTFILE = "products_and_aspects.json"

def find_aspects(product, posts):
	aspects = {}
	threshold = 0.2
	contains_product_count = 0

	for post in posts:
		if product.lower() not in post["post_message"]:
			continue

		contains_product_count += 1
		sentences = nltk.sent_tokenize(post["post_message"])
		pos_sents = nltk.sent_tokenize(post["pos_tagged"])
        
		for i, sentence in enumerate(sentences):
			try:
				if product.lower() not in sentence:
					continue
				adjectives = [x for x in pos_sents[i].split() if "NN" in x]
				if len(adjectives) != 0:
					for adjective in adjectives:
						adj = adjective.split("/")[0]
						if adj not in aspects:
							aspects[adj] = 0
						aspects[adj] += 1
			except IndexError:
				continue

	aspects = [k for k, v in aspects.items() if float(v)/contains_product_count >= threshold]

	return aspects

def merge_similar_entities(entities):
	from nltk.stem import WordNetLemmatizer
	lemmatizer = WordNetLemmatizer()
	result = {}

	for product, aspects in entities.items():
		parts = product.split()
		temp = " ".join(lemmatizer.lemmatize(part) for part in parts)
		if temp not in result:
			result[temp] = []
		result[temp] += aspects

	for product, aspects in result.items():
		merged_aspects = []
		for aspect in aspects:
			parts = aspect.split()
			temp = " ".join(lemmatizer.lemmatize(part) for part in parts)
			if temp not in merged_aspects:
				merged_aspects.append(temp)
		result[product] = merged_aspects

	return result

if __name__ == "__main__":
	dictionary = dict()

	with open(POSTSFILE, "r") as postf:
		posts = json.load(postf)

	with open(INFILE, "r") as inf:
		with open(OUTFILE, "w") as outf:
			products = json.load(inf)
			for idx, product in enumerate(products):
				dictionary[product] = ["general"]
				dictionary[product] += find_aspects(product, posts)
				print("Processed product {}".format(idx))
			
			dictionary = merge_similar_entities(dictionary)
			json.dump(dictionary, outf, indent=2)