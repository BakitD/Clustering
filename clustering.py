from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

def cluster(trends, model, n_clusters=5):
	cluster_list = prepare_list(trends, model)
	kmeans = KMeans(init='k-means++', n_clusters=n_clusters)
	kmeans.fit(cluster_list[1])
	return prepare_results(cluster_list, kmeans.labels_, n_clusters)


def prepare_list(trends, model):
	cluster_list = [[],[]]
	for key, value in trends.iteritems():
		cluster_list[0].append(key)
		cluster_list[1].append(model[value[0].lower()])
	return cluster_list

def prepare_results(cluster_list, indexes, n_clusters):
	result = {}
	for i in range (0, len(indexes)):
		if not result.get(indexes[i]): result[indexes[i]] = []
		result[indexes[i]].append(cluster_list[0][i])
	return result


def cluster_aggl(trends, model, n_clusters=5):
	cluster_list = prepare_list(trends, model)
	kmeans = AgglomerativeClustering(n_clusters=n_clusters, affinity='cosine',
					linkage='complete')
	kmeans.fit(cluster_list[1])
	return prepare_results(cluster_list, kmeans.labels_, n_clusters)


def cluster_words(trends, model, n_clusters):
	words = list(set([word for lst in trends.values() for word in lst]))
	words_vectors = [model[word.lower()] for word in words]
	#kmeans = KMeans(init='k-means++', n_clusters=n_clusters)
	kmeans = AgglomerativeClustering(n_clusters=n_clusters, affinity='cosine',
					linkage='complete')
	kmeans.fit(words_vectors)
	clusters = {}
	#print kmeans.labels_
	for i in range(0, len(kmeans.labels_)):
		if not clusters.get(kmeans.labels_[i]):
			clusters[kmeans.labels_[i]] = [words[i]]
		else:
			clusters[kmeans.labels_[i]].append(words[i])
	return clusters

