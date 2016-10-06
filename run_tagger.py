import sys
import json
from language_model import *
from witten_bell_smoothing import *

def read_model(filename):
	with open(filename) as model_file:
		data = json.load(model_file)
		return data

def read_test(filename):
	with open(filename) as test_file:
		return list(map(lambda line: list(line[:-1].split()), test_file.readlines()))

def write_tagged_sent_to_file(sents, filename):
	with open(filename, 'w') as out_file:
		for sent in sents:
			out_file.write(sent)
			out_file.write('\n')

def viterbi(model, sent):
	tags = model.getTagList()
	tag_size = len(tags)
	sent_size = len(sent)
	#print('tags: ', tag_size, ', sentence: ', sent_size)
	
	witten_bell = WittenBellSmoothing(model)

	# Initialize memo to store Viterbi states.
	memo = []
	for i in range(tag_size):
		memo_row = []
		for j in range(sent_size):
			memo_row.append([-123123123, -1])
		memo.append(memo_row)

	# Initialize start of sentence.
	for i in range(tag_size):
		prob = witten_bell.getProbTagGivenTag('<s>', tags[i]) + witten_bell.getProbWordGivenTag(tags[i], sent[0])
		memo[i][0][0] = prob
		memo[i][0][1] = 0
	
	# Go through Viterbi's algorithm.
	for j in range(1, sent_size):
		for i in range(tag_size):
			for k in range(tag_size):
				prob = memo[k][j-1][0] + witten_bell.getProbTagGivenTag(tags[k], tags[i])
				if prob > memo[i][j][0]:
					memo[i][j][0] = prob
					memo[i][j][1] = k
			memo[i][j][0] += witten_bell.getProbWordGivenTag(tags[i], sent[j])

	# Process end of sentence.
	final_max, final_backpointer = -123123123,-1
	for i in range(tag_size):
		prob = memo[i][len(sent)-1][0] + witten_bell.getProbTagGivenTag(tags[i], '</s>')
		if prob > final_max:
			final_max = prob
			final_backpointer = i

	# print(final_backpointer)
	# for i in range(tag_size):
	# 	backpointers = []
	# 	for j in range(sent_size):
	# 		backpointers.append(memo[i][j][1])
	# 	print(i, tags[i], backpointers)

	# Trace back the backpointers to obtain POS tag sequence.
	pointer = final_backpointer
	sent_idx = sent_size-1
	sequence = []
	while sent_idx >= 0:
		sequence.append(tags[pointer])
		pointer = memo[pointer][sent_idx][1]
		sent_idx -= 1
	sequence.reverse()

	tagged_sent = []
	for idx in range(sent_size):
		tagged_sent.append(sent[idx] + '/' + sequence[idx])
	return tagged_sent

if __name__ == "__main__":
	test_filename = ''
	model_filename = ''
	output_filename = ''
	if len(sys.argv) < 4:
		print('Wrong format!')
		print('run_tagger.py <test filename> <model filename> <output filename>')
		sys.exit(2)
	test_filename, model_filename, output_filename = sys.argv[1:]
	model = LanguageModel(read_model(model_filename))
	test_sents = read_test(test_filename)
	tagged_test_sents = list(map(lambda sent: ' '.join(viterbi(model, sent)), test_sents))
	write_tagged_sent_to_file(tagged_test_sents, output_filename)