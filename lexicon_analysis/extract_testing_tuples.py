import json
import nltk

INFILE = "../tagging/complete_tagged.json"
OUTFILE = "testing_posts.json"
PRODUCTFILE = "../extraction/products_and_aspects.json"

def find_posts(product, aspects, num_posts, posts):
	result = []

	for post in posts:
		post_message = post["post_message"].lower()

		if product.lower() not in post_message:
			continue

		post["sentiments"] = []
		sentences = nltk.sent_tokenize(post_message)

		for sentence in sentences:
			if product.lower() not in sentence:
				continue

			aspects_found = False
			for aspect in aspects:
				if aspect not in sentence:
					continue

				post["sentiments"].append((product, aspect, "unknown"))
				aspect_found = True

			if not aspect_found:
				post["sentiments"].append((product, "general", "unknown"))

		if len(post["sentiments"]) > 0:
			result.append(post)
			if len(result) == num_posts:
				break

	return result



if __name__ == "__main__":
	num_posts = 200
	product = "Customer Service"

	with open(INFILE, "r") as inf:
		posts = json.load(inf)

	with open(PRODUCTFILE, "r") as prodf:
		products = json.load(prodf)

	if product not in products:
		raise ValueError("The given product is not present in the dictionary.")

	mentioning_posts = find_posts(product, products[product], num_posts, posts)

	with open(OUTFILE, "w") as outf:
		json.dump(mentioning_posts, outf, indent=2)
