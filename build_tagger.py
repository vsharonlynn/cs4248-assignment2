import sys
import json
from language_model import *

def read_data(filename):
    with open(filename, 'r') as infile:
        return list(map(lambda line: list(map(lambda pair: list(pair.rsplit('/', 1)), line[:-1].split())), infile.readlines()))

def write_json_to_file(json_data, filename):
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile, ensure_ascii=False, indent=4, sort_keys=True)

def generate_counts(model, data):
    for line in data:
        for idx in range(len(line)+1):
            if idx < len(line):
                word, pos = line[idx]
                model.add_tag_word(pos, word)
                model.add_wordtype(word)
            else:
                pos = '</s>'
            model.add_tag(pos)

            if idx > 0:
                prev_pos = line[idx-1][1]
            else:
                prev_pos = '<s>'
                model.add_tag(prev_pos)
            model.add_tag_tag(prev_pos, pos)

if __name__ == "__main__":
    train_filename = ''
    devt_filename = ''
    model_filename = ''
    if len(sys.argv) < 4:
        print("Wrong Format!")
        print("build_tagger.py <train filename> <devt filename> <model filename>")
        sys.exit(2)
    train_filename, devt_filename, model_filename = sys.argv[1:]
    data1 = read_data(train_filename)
    data2 = read_data(devt_filename)
    language_model = LanguageModel()
    generate_counts(language_model, data1)
    generate_counts(language_model, data2)
    write_json_to_file(language_model.counts, model_filename)
