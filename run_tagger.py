import sys
import json
import math

def read_model(filename):
	with open(filename) as model_file:
		data = json.load(model_file)
		return data

def read_test(filename):
	with open(filename) as test_file:
		return list(map(lambda line: list(line[:-1].split()), test_file.readlines()))

def getTagCount(model, tag):
	if tag in model['tag_count']:
		return model['tag_count'][tag]
	else:
		return 0

# Tag - Tag
def getTotalTags(model):
	return len(model['tag_count'].keys())

def getTagSeenTags(model, tag):
	tags = list(model['tag_given_tag'][tag]['content'].keys())
	return len(tags)

def getTagUnseenTags(model, tag):
	return getTotalTags(model) - getTagSeenTags(model, tag)

def getCountTagTag(model, prev_tag, curr_tag):
	if curr_tag not in model['tag_given_tag'][prev_tag]['content']:
		return 0
	else:
		return model['tag_given_tag'][prev_tag]['content'][curr_tag]

def getProbTagGivenTag(model, prev_tag, curr_tag):
	count_tag_tag = getCountTagTag(model, prev_tag, curr_tag)
	count_tag = getTagCount(model, prev_tag)
	seen_tag = getTagSeenTags(model, prev_tag)
	unseen_tag = getTagUnseenTags(model, prev_tag)
	if count_tag_tag > 0.0:
		prob = count_tag_tag / (count_tag + seen_tag)
	else:
		prob = count_tag / (unseen_tag * (count_tag + seen_tag))
	return math.log10(prob)

# Tag - Word
def getTotalWordTypes(model):
	return len(model['wordtype_count'].keys())

def getTagSeenWords(model, tag):
	return len(model['word_given_tag'][tag]['content'].keys())

def getTagUnseenWords(model, tag):
	return getTotalWordTypes(model) - getTagSeenWords(model, tag)

def getCountTagWord(model, tag, word):
	if word not in model['word_given_tag'][tag]['content']:
		return 0
	else:
		return model['word_given_tag'][tag]['content'][word]

def getProbWordGivenTag(model, tag, word):
	count_tag_word = getCountTagWord(model, tag, word)
	count_tag = getTagCount(model, tag)
	seen_words = getTagSeenWords(model, tag)
	unseen_words = getTagUnseenWords(model, tag)
	if count_tag_word > 0:
		prob = count_tag_word / (count_tag + seen_words)
	else:
		prob = count_tag / (unseen_words * (count_tag + seen_words))
	return math.log10(prob)

def viterbi(model, sent):
	tags = list(model['tag_count'].keys())
	if '<s>' in tags:
		tags.remove('<s>')
	if '</s>' in tags:
		tags.remove('</s>')
	print(tags)
	tag_size = len(tags)
	sent_size = len(sent)
	print('tags: ', tag_size, ', sentence: ', sent_size)
	memo = []
	for i in range(tag_size):
		memo_row = []
		for j in range(sent_size):
			memo_row.append([-123123123, -1])
		memo.append(memo_row)
	#print(memo)

	# Init first column
	for i in range(tag_size):
		prob = getProbTagGivenTag(model, '<s>', tags[i]) + getProbWordGivenTag(model, tags[i], sent[0])
		memo[i][0][0] = prob
		memo[i][0][1] = 0
	

if __name__ == "__main__":
	test_filename = ''
	model_filename = ''
	output_filename = ''
	if len(sys.argv) < 4:
		print('Wrong format!')
		print('run_tagger.py <test filename> <model filename> <output filename>')
		sys.exit(2)
	test_filename, model_filename, output_filename = sys.argv[1:]
	model = read_model(model_filename)
	#print(model)
	test = read_test(test_filename)
	#print(test[:5])
	viterbi(model, test[0])