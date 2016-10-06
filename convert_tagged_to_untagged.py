import sys

def read_file(filename):
    with open(filename, 'r') as in_file:
        return list(map(lambda line: list(map(lambda pair: list(pair.rsplit('/', 1)), line[:-1].split())), in_file.readlines()))

def write_data(data, filename):
	with open(filename, 'w') as out_file:
		for sent in data:
			s = ' '.join(sent)
			out_file.write(s)
			out_file.write('\n')

def convert_train_to_test(in_file, out_file):
	data = read_file(in_file)
	cleaned_data = []
	for line in data:
		clean_line = list(map(lambda pair: pair[0], line))
		cleaned_data.append(clean_line)
	write_data(cleaned_data, out_file)


if __name__ == "__main__":
	in_file, out_file = sys.argv[1:]
	convert_train_to_test(in_file, out_file)