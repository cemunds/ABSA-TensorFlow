#!/usr/bin/python3
import logging
import json

logging.basicConfig(level=logging.INFO)
INFILE = 'posts.json'
OUTFILE = 'posts_preprocessed.json'
MIN_TEXT_LENGTH = 20


def preprocess(data):
    logging.info("Preprocessing data")
    results = []
    for post in data:
        if len(post['post_message']) < MIN_TEXT_LENGTH or post['type'] == "photo":
            logging.debug("removed post {}".format(post["post_id"]))
            continue
        else:
            post["post_message_lowered"] = post["post_message"].lower()
            results.append(post)
    return results
                    
if __name__ == "__main__":
    with open(INFILE, "r") as inf:
        with open(OUTFILE, "w") as outf:
            posts = json.load(inf)
            result = preprocess(posts)
            json.dump(result, outf, indent=2)