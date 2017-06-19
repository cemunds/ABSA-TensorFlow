#!/usr/bin/python3
import os
import json
import logging

logging.basicConfig(level=logging.INFO)

OUTFILE = "posts.json"
SUBDIR = "Tesco"

datafilter = [0, 2, 4, 11]
filter_names = ["type", "post_id", "post_message", "post_published_sql"]

def parse_data():
    logging.info("Parsing data")
    final_result = []
    for root, directory, filenames in os.walk(SUBDIR):
        for filename in filenames:
            if '.tab' in filename and 'fullstats' in filename:
                fullfilename = os.path.join(root, filename)
                logging.info("Processing file {}".format(fullfilename))
                with open(fullfilename, 'r', encoding="utf8") as fin:
                    for idx, line in enumerate(fin):
                        if idx == 0:
                            continue
                        else:
                            line = line.split("\t")
                            result = {}
                            for i, f in enumerate(datafilter):
                                result[filter_names[i]] = line[f]
                            final_result.append(result)
    return final_result

if __name__ == "__main__":
    result = parse_data()
    with open(OUTFILE, "w") as outf:
        json.dump(result, outf, indent=2)