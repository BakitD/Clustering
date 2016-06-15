import MySQLdb as mysql
from contextlib import closing
from settings import DB

db = mysql.connect(host=DB.host, user=DB.user, \
			passwd=DB.password, db=DB.db, 
			charset='utf8', \
			init_command='set names utf8')

def drop_clusters():
	cursor = db.cursor()
	cursor.execute('delete from clusters;')
	trends = cursor.fetchall()
	db.commit()


def get_themes():
	cursor = db.cursor()
	cursor.execute('select name from trend;')
	trends = cursor.fetchall()
	return [x[0] for x in trends]

def save_clusters(clusters, trends):
	with closing(db.cursor(mysql.cursors.DictCursor)) as cursor:
		cluster_index = 0
		for cluster_id in range(0, len(clusters)):
			cursor.execute("insert into clusters (name) values (%s);", (str(cluster_id),))
			cluster_rowid = cursor.lastrowid
			for word in clusters[cluster_id]:
				cursor.execute("insert into word (name, clusters_id) values (%s, %s);", \
						(word, cluster_rowid))
			db.commit()
		for trend, values in trends.iteritems():
			for word in values:
				#print trend, word
				cursor.execute("insert into trendword (trend_id, word_id) values " \
					"((select id from trend where name = %s), " \
					"(select id from word where binary name = %s));", (trend, word))
		db.commit()
	db.close()
	
