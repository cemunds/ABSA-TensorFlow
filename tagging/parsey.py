#!/usr/bin/python2.7
import os
import json
import logging
import subprocess
INFILE = '../data/posts_preprocessed.json'
OUTFILE = 'posts_pos_parsey.json'
SYNTAXNET_DIR = r"/home/ric/projects/models/syntaxnet"
PARSER_EVAL = r"bazel-bin/syntaxnet/parser_eval"
MODEL_DIR = r"syntaxnet/models/parsey_mcparseface"
logging.basicConfig(level=logging.INFO)

def parse_sentence(sentence):
    os.chdir(SYNTAXNET_DIR)
    cmd = "echo \"{2}\" | {1} --input=stdin --output=stdout-conll --hidden_layer_sizes=64 --arg_prefix=brain_tagger --graph_builder=structured --task_context={0}/context.pbtxt --model_path={0}/tagger-params --slim_model --batch_size=1024 --alsologtostderr".format(MODEL_DIR, PARSER_EVAL, sentence)
    parse = subprocess.check_output([cmd], shell = True, stderr = subprocess.STDOUT)
    return parse

def process_parse(parse):
    conll = []
    for i in reversed(parse.split('\n')):
        if "tensorflow" in i.lower():
            break
        elif len(i) > 0:
            conll.append(i)
    pos = []
    for word in reversed(conll):
        parts = word.split('\t')
        pos_word = parts[1]
        try:
            pos_part = [i for i in parts[2:] if not '_' in i and not '0' in i][0]
            pos.append([pos_word, pos_part])
        except:
            continue
    return pos

if __name__=="__main__":
    with open(INFILE, 'r') as fin:
        with open(OUTFILE, 'w') as fout:
            result = []
            data = json.load(fin)
            for i, post in enumerate(data):
                logging.info("{}/{}\tProcessing {}".format(i,len(data),post["post_id"]))
                try:
                    message = post["post_message"].encode('ascii', 'ignore')
                    parse = parse_sentence(message)
                    pos = process_parse(parse)
                    post["post_message_pos_parsey"] = pos
                except:
                    logging.warning("Could not extract post data")
                result.append(post)
            json.dump(result, fout)
