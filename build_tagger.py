import sys
import json

def read_data(filename):
    with open(filename, 'r') as infile:
        return list(map(lambda line: list(map(lambda pair: list(pair.rsplit('/', 1)), line[:-1].split())), infile.readlines()))

def write_json_to_file(json_data, filename):
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, ensure_ascii=False, indent=4, sort_keys=True)

def generate_counts(counts, data):
    for line in data:
        for idx in range(len(line)+1):
            if idx < len(line):
                word, pos = line[idx]
                if pos not in counts['word_given_pos']:
                    counts['word_given_pos'][pos] = {'total':0, 'content':{}}
                if word not in counts['word_given_pos'][pos]['content']:
                    counts['word_given_pos'][pos]['content'][word] = 0
                counts['word_given_pos'][pos]['content'][word] += 1
                counts['word_given_pos'][pos]['total'] += 1
            else:
                pos = '</s>'

            if idx > 0:
                prev_pos = line[idx-1][1]
            else:
                prev_pos = '<s>'
            if prev_pos not in counts['pos_given_pos']:
                counts['pos_given_pos'][prev_pos] = {'total':0, 'content':{}}
            if pos not in counts['pos_given_pos'][prev_pos]['content']:
                counts['pos_given_pos'][prev_pos]['content'][pos] = 0
            counts['pos_given_pos'][prev_pos]['content'][pos] += 1
            counts['pos_given_pos'][prev_pos]['total'] += 1
    return counts

if __name__ == "__main__":
    train_filename = ''
    devt_filename = ''
    model_filename = ''
    if len(sys.argv) < 4:
        print("Wrong Format!")
        print("build_tagger.py <train file_name> <devt file_name> <model filename>")
        sys.exit(2)
    train_filename, devt_filename, model_filename = sys.argv[1:]
    data = read_data(train_filename)
    counts = {
        'pos_given_pos': {},
        'word_given_pos': {},
    }
    generate_counts(counts, data)
    write_json_to_file(counts, model_filename)
