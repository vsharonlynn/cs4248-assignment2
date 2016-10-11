# Main Scripts
## Train the POS Tagger
```sh
python build_tagger.py <train_filename> <devt_filename> <model_filename>
```
Example:
```sh
python build_tagger.py sents.train sents.devt model_file
```

## Run the POS Tagger
```sh
python run_tagger.py <test_filename> <model_filename> <output_filename>
```
Example:
```sh
python run_tagger.py sents.test model_file out_file
```

# Additional Scripts for Testing
To convert a tagged data (e.g. train or development data) to untagged data:
```sh
python convert_tagged_to_untagged.py <tagged_filename> <output_filename>
```
Example:
```sh
python convert_tagged_to_untagged.py sents_small.devt sents_small.test
```

To compare between original tagged and generate tagged files:
```sh
python compare.py <original_tagged_filename> <generated_tagged_filename>
```
Example:
```sh
python compare.py sents_small.devt out_file
```
