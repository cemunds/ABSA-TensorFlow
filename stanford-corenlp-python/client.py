#!/usr/bin/python2
import json
import time
import nltk
import logging
import os
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint
from nltk.tokenize.moses import MosesDetokenizer

#encoding=utf8
import sys

reload(sys)
#sys.setdefaultencoding('utf8')

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

data = parse_data()
data = preprocess(data)

logging.basicConfig(level=logging.INFO)
INFILE = "../data/posts_preprocessed.json"
OUTFILE = "posts_co-referenced.json"

import jsonrpclib

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))

    def parse(self, text):
        return json.loads(self.server.parse(text))


nlp = StanfordNLP()
detokenizer = MosesDetokenizer()

logging.info("Co-refing data")
results = []
for idx, post in enumerate(data):
    nlp = StanfordNLP()
#    post["post_message"] =  post["post_message"].encode('utf-8')
    post["post_message"] = unicode(post["post_message"], errors='ignore')
    if(len(post["post_message"]) > 750):
        continue
    pprint(post["post_message"])
    sentences = nltk.sent_tokenize(post["post_message"])
    words = [nltk.word_tokenize(s) for s in sentences]
    try:
        tmp = nlp.parse(post["post_message"])
        if('coref' in tmp):
            for arr in tmp['coref']:
                for arr2 in arr:
                        ref1 = arr2[0]
                        ref2 = arr2[1]
                        i = ref1[4] - 1 - ref1[3]
                        while i > 0:
                             i = i - 1
                             words[ref1[1]][ref1[3]] = ''
                        words[ref1[1]][ref1[3]] = ref2[0]
            newSentences = []
            for wordArrs in words:
                newSentences.append(detokenizer.detokenize(wordArrs, return_str=True))
            newPost = detokenizer.detokenize(newSentences, return_str=True)
            pprint(tmp['coref'])
            pprint(post["post_message"])
            pprint(newPost)
            post["post_message"] = newPost
            post["coref-changed"] = 1
            print('')
    except KeyboardInterrupt:
        sys.exit()
    except:
        pprint(post["post_message"])
        post["coref-changed"] = 0
        print('error occurred')
        print('')
        time.sleep(0.5)
    data[idx] = post

with open(OUTFILE, 'w') as outfile:
    json.dump(data, outfile)
