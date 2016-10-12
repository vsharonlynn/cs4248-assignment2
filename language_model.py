class LanguageModel:
	def __init__(self):
		self.counts = {
	        'tag_given_tag': {},
	        'word_given_tag': {},
	        'tag_count': {},
	        'wordtype_count': {},
	    }
		self.total_tag_count = None
		self.total_wordtype_count = None
		self.total_tag_given_tag_count = {}
		self.total_word_given_tag_count = {}

	def fromFile(self, preloaded_counts):
		self.counts = preloaded_counts

	def add_tag_word(self, tag, word):
		if tag not in self.counts['word_given_tag']:
			self.counts['word_given_tag'][tag] = {'total':0, 'content':{}}
		if word not in self.counts['word_given_tag'][tag]['content']:
			self.counts['word_given_tag'][tag]['content'][word] = 0
		self.counts['word_given_tag'][tag]['content'][word] += 1
		self.counts['word_given_tag'][tag]['total'] += 1

	def add_wordtype(self, word):
		if word not in self.counts['wordtype_count']:
			self.counts['wordtype_count'][word] = 0
		self.counts['wordtype_count'][word] += 1

	def add_tag(self, tag):
		if tag not in self.counts['tag_count']:
			self.counts['tag_count'][tag] = 0
		self.counts['tag_count'][tag] += 1

	def add_tag_tag(self, prev_tag, tag):
		if prev_tag not in self.counts['tag_given_tag']:
			self.counts['tag_given_tag'][prev_tag] = {'total':0, 'content':{}}
		if tag not in self.counts['tag_given_tag'][prev_tag]['content']:
			self.counts['tag_given_tag'][prev_tag]['content'][tag] = 0
		self.counts['tag_given_tag'][prev_tag]['content'][tag] += 1
		self.counts['tag_given_tag'][prev_tag]['total'] += 1

	def getTagCount(self, tag):
		if tag in self.counts['tag_count']:
			return self.counts['tag_count'][tag]
		else:
			return 0

	def getTagList(self):
		tags = list(self.counts['tag_count'].keys())
		if '<s>' in tags:
			tags.remove('<s>')
		if '</s>' in tags:
			tags.remove('</s>')
		return tags

	# Tag - Tag
	def getTotalTags(self):
		if self.total_tag_count == None:
			self.total_tag_count = len(self.counts['tag_count'])
		return self.total_tag_count

	def getTagSeenTags(self, tag):
		if tag not in self.total_tag_given_tag_count:
			self.total_tag_given_tag_count[tag] = len(self.counts['tag_given_tag'][tag]['content'])
		return self.total_tag_given_tag_count[tag]

	def getTagUnseenTags(self, tag):
		return self.getTotalTags() - self.getTagSeenTags(tag)

	def getCountTagTag(self, prev_tag, curr_tag):
		if curr_tag not in self.counts['tag_given_tag'][prev_tag]['content']:
			return 0
		else:
			return self.counts['tag_given_tag'][prev_tag]['content'][curr_tag]

	# Tag - Word
	def getTotalWordTypes(self):
		if self.total_wordtype_count == None:
			self.total_wordtype_count = len(self.counts['wordtype_count'])
		return self.total_wordtype_count

	def getTagSeenWords(self, tag):
		if tag not in self.total_word_given_tag_count:
			self.total_word_given_tag_count[tag] = len(self.counts['word_given_tag'][tag]['content'])
		return self.total_word_given_tag_count[tag]

	def getTagUnseenWords(self, tag):
		return self.getTotalWordTypes() - self.getTagSeenWords(tag)

	def getCountTagWord(self, tag, word):
		if word not in self.counts['word_given_tag'][tag]['content']:
			return 0
		else:
			return self.counts['word_given_tag'][tag]['content'][word]
