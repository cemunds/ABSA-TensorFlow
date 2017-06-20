import json
import nltk

POSTSFILE = "../tagging/complete_tagged.json"
INFILE = "products.json"
OUTFILE = "products_and_aspects.json"

def find_aspects(product, posts):
	aspects = {}
	threshold = 0.1
	contains_product_count = 0

	for post in posts:
		post_message = post["post_message"].lower()
		if product.lower() not in post_message:
			continue

		contains_product_count += 1
		sentences = nltk.sent_tokenize(post_message)
		pos_sents = nltk.sent_tokenize(post["pos_tagged"])
        
		for i, sentence in enumerate(sentences):
			try:
				if product.lower() not in sentence:
					continue

				potential_aspects = [x for x in pos_sents[i].split() if "/NN" in x]
				if len(potential_aspects) != 0:
					for potential_aspect in potential_aspects:
						asp = potential_aspect.split("/")[0].lower()
						if len(asp) <= 1:
							continue

						if asp not in aspects:
							aspects[asp] = 0
						aspects[asp] += 1
			except IndexError:
				continue

	aspects = [k for k, v in aspects.items() if float(v)/contains_product_count >= threshold]

	return aspects

def merge_similar_entities(entities):
	from nltk.stem import WordNetLemmatizer
	lemmatizer = WordNetLemmatizer()
	result = {}

	for product, aspects in entities.items():
		if " " in product:
			parts = product.split()
			# Align casing
			lemmatized_parts = [lemmatizer.lemmatize(part).capitalize() if part[0].isupper() else lemmatizer.lemmatize(part) for part in parts]
			product = " ".join(lemmatizer.lemmatize(part.lower()).capitalize() for part in parts)

		if product not in result:
			result[product] = []
		result[product] += aspects

	for product, aspects in result.items():
		merged_aspects = []
		for aspect in aspects:
			parts = aspect.split()
			aspect = " ".join(lemmatizer.lemmatize(part) for part in parts)
			if aspect not in merged_aspects:
				merged_aspects.append(aspect)
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
				print("Processing product {}".format(idx))
				aspects = find_aspects(product, posts)
				if len(aspects) == 0:
					continue

				dictionary[product] = ["general"]
				dictionary[product] += aspects
			
			print("Merging similar products and aspects")
			dictionary = merge_similar_entities(dictionary)
			json.dump(dictionary, outf, indent=2)