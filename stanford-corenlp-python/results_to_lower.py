#!/usr/bin/python3
import logging
import json
MIN_TEXT_LENGTH = 20

INFILE = 'posts_co-referenced.json'
OUTFILE = 'posts_co-referenced_lower.json'

def tolower(data):
    results = []
    for post in data:
        if len(post['coref_post_message']) < MIN_TEXT_LENGTH or post['type'] == "photo":
            logging.debug("removed post {}".format(post["post_id"]))
            continue
        else:
            post["coref_post_message_lowered"] = post["coref_post_message"].lower()
            results.append(post)
    return results

if __name__ == "__main__":
    with open(INFILE, "r") as inf:
        with open(OUTFILE, "w") as outf:
            posts = json.load(inf)
            result = tolower(posts)
            json.dump(result, outf, indent=2)
