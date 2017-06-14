cort-predict-raw -in *.txt -model model-tree-train+dev.obj -extractor cort.coreference.approaches.mention_ranking.extract_substructures -perceptron cort.coreference.approaches.mention_ranking.RankingPerceptron -clusterer cort.coreference.clusterer.all_ante -corenlp stanford-corenlp-full-2017-06-09

