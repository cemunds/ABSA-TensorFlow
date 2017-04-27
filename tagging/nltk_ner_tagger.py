import nltk
import json

INFILE = "posts_pos_tagged.json"
OUTFILE = "posts_ner_tagged.json"

results = []
grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
      {<NNP>+}                # chunk sequences of proper nouns
"""
cp = nltk.RegexpParser(grammar)

with open(INFILE, "r") as inf:
	with open(OUTFILE, "w") as outf:
		posts = json.load(inf)
		for post in posts:

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
						post["noun_phrases"].append(str(subtree))

			trees = [nltk.ne_chunk(sentence, binary=True) for sentence in sentences]
			post["entities"] = []
			for tree in trees:
				for subtree in tree.subtrees():
					if subtree.label() == "NE":
						post["entities"].append(str(subtree))
			results.append(post)
		json.dump(results, outf, indent=2)