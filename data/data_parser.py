#!/usr/bin/python3
import os
import logging

logging.basicConfig(level=logging.INFO)
SUBDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Tesco')

datafilter = [0, 2, 4, 11]
filter_names = ["type", "post_id", "post_message", "post_published_sql"]

def parse_data():
    logging.info("Parsing data")
    logging.debug("nparse_data path : {}".format(SUBDIR))
    final_result = []
    for root, directory, filenames in os.walk(SUBDIR):
        for filename in filenames:
            if '.tab' in filename and 'fullstats' in filename:
                fullfilename = os.path.join(root, filename)
                logging.debug("Processing file {}".format(fullfilename))
                with open(fullfilename, 'r') as fin:
                    for idx, line in enumerate(fin.readlines()):
                        if idx == 0:
                            continue
                        else:
                            line = line.split("\t")
                            result = {}
                            for i, f in enumerate(datafilter):
                                result[filter_names[i]] = line[f]
                            final_result.append(result)
    return final_result




