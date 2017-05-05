import logging
import time
from data import data_parser, data_preprocess
from tagging import nltk_pos_tagger, nltk_ner_tagger
from informationminer import InformationMiner

logging.basicConfig(level=logging.DEBUG)
USE_INFORMATIONMINER = True

if __name__ == '__main__':
    parsed = data_parser.parse_data()
    preprocessed = data_preprocess.preprocess(parsed)
    if USE_INFORMATIONMINER:
        start = time.time()
        im = InformationMiner([p["post_message"] for p in preprocessed], language="en", save_output=True, outdir="im_out")
        im.process()
        end = time.time()
        logging.info("Took {:.2f} s".format(end - start))
    else:
        start = time.time()
        pos = nltk_pos_tagger.tag(preprocessed)
        ner = nltk_ner_tagger.tag(preprocessed)
        end = time.time()
        logging.info("Took {:.2f} s".format(end - start))
