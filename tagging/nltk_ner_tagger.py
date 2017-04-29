import nltk
import json
import numpy as np

INFILE = "posts_pos_tagged.json"
OUTFILE = "posts_ner_tagged.json"
TAGS = ["DT", "PP", "JJ", "NN", "NNP"]

results = []
grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
      {<NNP>+}                # chunk sequences of proper nouns
"""
cp = nltk.RegexpParser(grammar)

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		posts = json.load(inf)
		for idx, post in enumerate(posts):

			sentences = []
			for sentence in post["post_message_pos_tagged_nltk"]:
				tokens = []
				for token in sentence:
					tokens.append(tuple(token))
				sentences.append(tokens)

			trees = [cp.parse(sentence) for sentence in sentences]
			post["noun_phrases"] = []
			for tree in trees:
				for subtree in tree.subtrees():
					if subtree.label() == "NP":
						# (NP a/DT massive/JJ big/JJ thank/NN) => a/DT massive/JJ big/JJ thank/NN
						post["noun_phrases"].append(str(subtree)[4:-1])

			trees = [nltk.ne_chunk(sentence, binary=True) for sentence in sentences]
			post["entities"] = []
			for tree in trees:
				for subtree in tree.subtrees():
					if subtree.label() == "NE":
						# Make (NE Mastercard/NNP) to mastercard
						temp = str(subtree)[4:-1]
						temp = temp.split()
						temp = [x.split("/") for x in temp]
						temp = filter(lambda x: x not in TAGS, np.array(temp).flatten())

						post["entities"].append(" ".join(x.lower() for x in temp))
			results.append(post)
			print("Processed post {}".format(idx))
		json.dump(results, outf, indent=2)