#!/usr/bin/python3
import os
import json
INFILE = 'posts.json'
OUTFILE = 'posts_preprocessed.json'
MIN_TEXT_LENGTH = 20


with open(OUTFILE, 'w') as fout:
    results = []
    with open(INFILE, 'r') as fin:
        for post in json.load(fin):
            if len(post['post_message']) < MIN_TEXT_LENGTH or post['type'] == "photo":
                print("removed post {}".format(post["post_id"]))
                continue
            else:
                results.append(post)
    json.dump(results, fout, indent=2)
                    
                        
