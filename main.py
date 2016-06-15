import re
import logging

import database as db
import trendfilter
import clustering
from gensim.models.word2vec import Word2Vec

from settings import CLUSTER_NUM, ModelSettings

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

model = Word2Vec.load_word2vec_format(ModelSettings.filename, binary=ModelSettings.binary)

def main():
	# Get all trends from database
	db.drop_clusters()
	themes = db.get_themes()
	tfilter = trendfilter.TrendFilter(model)
	tfilter.makeFiltration(themes)

	#clusters = clustering.cluster(w2v_words, model, 20)
	#clusters = clustering.cluster_aggl(w2v_words, model, 20)
	#for key, value in clusters.iteritems():
	#	print value, '\n\n'
	#print tfilter.w2v_words
	clusters = clustering.cluster_words(tfilter.w2v_words, model, CLUSTER_NUM)
	for cluster in clusters.values(): print cluster, '\n\n'
	db.save_clusters(clusters, tfilter.w2v_words)
	tfilter.get_statinfo()

main()
