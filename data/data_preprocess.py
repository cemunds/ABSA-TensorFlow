#!/usr/bin/python3
import logging

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
            results.append(post)
    return results
                    
                        
