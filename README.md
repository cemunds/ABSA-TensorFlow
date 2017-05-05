## Work Flow

### Option 1
Use process.py to automaticall execute the scripts

### Option 2
Manually use the scripts as following

#### data
data_parser.py => posts.json
data_parser_preprocess.py => posts_preprocessed.json

#### tagging
nltk_pos_tagger.py => posts_pos_tagged.json
nltk_ner_tagger.py => posts_ner_tagged.json

#### extraction
extract_frequent_nouns.py => extracted_entities.json
apply_blacklist.py => extracted_entities_cleaned.json
assign_entities_to_posts.py => posts_assigned_entities.json

#### lexicon_analysis
mark_sentiment_words.py => posts_marked_sentiment_words.json
