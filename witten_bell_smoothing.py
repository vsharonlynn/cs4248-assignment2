from __future__ import division
import math

class WittenBellSmoothing:
	model = {}

	def __init__(self, model):
		self.model = model

	def getProbTagGivenTag(self, prev_tag, curr_tag):
		count_tag_tag = self.model.getCountTagTag(prev_tag, curr_tag)
		count_tag = self.model.getTagCount(prev_tag)
		seen_tag = self.model.getTagSeenTags(prev_tag)
		unseen_tag = self.model.getTagUnseenTags(prev_tag)
		if count_tag_tag > 0.0:
			prob = count_tag_tag / (count_tag + seen_tag)
		else:
			prob = count_tag / (unseen_tag * (count_tag + seen_tag))
		return math.log10(prob)

	def getProbWordGivenTag(self, tag, word):
		count_tag_word = self.model.getCountTagWord(tag, word)
		count_tag = self.model.getTagCount(tag)
		seen_words = self.model.getTagSeenWords(tag)
		unseen_words = self.model.getTagUnseenWords(tag)
		if count_tag_word > 0:
			prob = count_tag_word / (count_tag + seen_words)
		else:
			prob = count_tag / (unseen_words * (count_tag + seen_words))
		return math.log10(prob)
