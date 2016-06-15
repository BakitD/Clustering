import re
import enchant

from settings import FilterSettings

class TrendFilter:
	def __init__(self, model):
		self.initial_trend_number = 0
		self.model = model
		self.english_words = None
		self.splitted_words = None
		self.mean_words = None
		self.w2v_words = None
		self.edict = enchant.Dict(FilterSettings.ENCHANT_DICT_TYPE)

	def get_statinfo(self):
		print 'Trends number: ', self.initial_trend_number
		print 'Number of words with ascii symbols: ', len(self.english_words)
		print 'Number of words with meaning: ', len(self.mean_words)
		print 'Final number of words: ', len(self.w2v_words)


	# Filter words taht contains english symbols and digits
	def isenglish(self, word):
		try:
			word.decode('ascii')
		except (UnicodeDecodeError, UnicodeEncodeError):
			return False
		else:
			return True

	def special_match(self, strg, search=re.compile(FilterSettings.PASS_WORDS_REGEXP).search):
		return not bool(search(strg))


	def filterEnglish(self, trends):
		result = []
		for trend in trends:
			if not self.isenglish(trend): continue
			if not self.special_match(trend): continue
			result.append(trend)
		return result



	# Picks out words and digits from word
	def extrude(self, word):
		return filter(None, re.findall(FilterSettings.WORDS_DIVIDER_REGEXP, word))



	def splitWords(self, trends):
		result = {}
		for trend in trends:
			split_word = trend.lstrip()
			if ' ' in split_word:
				result[trend] = []
				for word in split_word.split(' '):
					result[split_word] += self.extrude(split_word)
			else:
				result[trend] = self.extrude(split_word)
		return result


	def ismean(self, word_list):
		result = []
		for i in range(0, len(word_list)):
			if self.edict.check(word_list[i]):
				result.append(word_list[i])
			elif i > 0:
				new_word = word_list[i-1][-1] + word_list[i]
				if self.edict.check(new_word):
					result.append(new_word)
		return result

	# Check if words in trend has some meaning
	def filterMeaning(self, trends):
		result = {}
		for key, value in trends.iteritems():
			mres = self.ismean(value)
			if mres: result[key] = mres
			#result[key] = {'words' : value, 'mean_words' : ismean(value)}
		return result



	def filterModel(self, trends):
		result = {}
		for key, words in trends.iteritems():
			result[key] = []
			for word in words:
				try:
					self.model[word.lower()]
				except KeyError:
					pass
				else:
					if word not in FilterSettings.DELETE_WORDS:
						result[key].append(word)
			result[key] = list(set(result[key]))
			if not result[key]: del result[key]
		return result



	def makeFiltration(self, themes):
		self.initial_trend_number = len(themes)
		# Filter words with non english symbols in trend
		self.english_words = self.filterEnglish(themes)
		# Pick out words and digits in trend
		self.splitted_words = self.splitWords(self.english_words)
		#for key, value in splitted_words.iteritems():
		#	print key, value
		self.mean_words = self.filterMeaning(self.splitted_words)
		# Filter words according to dictionary
		self.w2v_words = self.filterModel(self.mean_words)
		#for key, value in w2v_words.iteritems():
		#	print key, value




