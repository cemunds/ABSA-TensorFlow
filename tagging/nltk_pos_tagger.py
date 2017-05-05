import nltk
import logging

logging.basicConfig(level=logging.INFO)
INFILE = "../data/posts_preprocessed.json"
OUTFILE = "posts_pos_tagged.json"


def tag(data):
    logging.info("NER tagging data")
    results = []
    for idx, post in enumerate(data):
        sentences = nltk.sent_tokenize(post["post_message"])
        words = [nltk.word_tokenize(s) for s in sentences]
        post["post_message_pos_tagged_nltk"] = [nltk.pos_tag(sentence) for sentence in words]
        results.append(post)
        logging.debug("Processed post {}".format(idx))
    return results
