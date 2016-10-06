import sys

def read_file(filename):
    with open(filename, 'r') as in_file:
        return list(map(lambda line: list(map(lambda pair: list(pair.rsplit('/', 1)), line[:-1].split())), in_file.readlines()))

if __name__ == "__main__":
	file1, file2 = sys.argv[1:]
	data1 = read_file(file1)
	data2 = read_file(file2)

	total, total_match = 0, 0
	for i, sentence in enumerate(data1):
		total += len(sentence)
		for j, word in enumerate(sentence):
			if word == data2[i][j]:
				total_match += 1
	print(total_match * 100.0 / total)