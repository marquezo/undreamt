Trying out Artetxe's UNdreaMT on English-Basque
==================

Requirements
--------
- Python 3
- PyTorch (tested with v0.3)
- NLTK
- tqdm

Order of pre-processing should be:

* `bash prep_eu_wiki.sh`
* `bash prep_en_data.sh`
* `bash download_embeddings.sh`
* `python extract_vocab.py cc.eu.300.vec vocab.eu train_vocab.eu`
* `python extract_vocab.py wiki-news-300d-1M.vec vocab.en train_vocab.en`
* `python update_corpus.py sentences.en train_vocab.en train_sentences.en`
* `python update_corpus.py sentences.eu train_vocab.eu train_sentences.eu`

Then to use vecmap we need to git clone it

* `cd vecmap`
* `nohup python3 map_embeddings,py --semi_supervised ../undreamt/train_dict.txt ../undreamt/train_emb.en ../undreamt/train_emb.eu ../undreamt/train_emb_mapped.en ../undreamt/train_emb_mapped.eu > out.log &`


Usage
--------

The following command trains an unsupervised NMT system from monolingual corpora using the exact same settings described in the paper:

```
python3 train.py --src SRC.MONO.TXT --trg TRG.MONO.TXT --src_embeddings SRC.EMB.TXT --trg_embeddings TRG.EMB.TXT --save MODEL_PREFIX --cuda
```

The data in the above command should be provided as follows:
- `SRC.MONO.TXT` and `TRG.MONO.TXT` are the source and target language monolingual corpora. They should both be pre-processed so atomic symbols (either tokens or BPE units) are separated by whitespaces. For that purpose, we recommend using [Moses](http://www.statmt.org/moses/) to tokenize and truecase the corpora and, optionally, [Subword-NMT](https://github.com/rsennrich/subword-nmt) if you want to use BPE.
- `SRC.EMB.TXT` and `TRG.EMB.TXT` are the source and target language cross-lingual embeddings. In order to obtain them, we recommend training monolingual embeddings in the corpora above using either [word2vec](https://github.com/tmikolov/word2vec) or [fasttext](https://github.com/facebookresearch/fastText), and then map them to a shared space using [VecMap](https://github.com/artetxem/vecmap). Please make sure to cutoff the vocabulary as desired before mapping the embeddings.
- `MODEL_PREFIX` is the prefix of the output model.

Using the above settings, training takes about 3 days in a single Titan Xp. Once training is done, you can use the resulting model for translation as follows:

```
python3 translate.py MODEL_PREFIX.final.src2trg.pth < INPUT.TXT > OUTPUT.TXT
```

For more details and additional options, run the above scripts with the `--help` flag.

License
-------

Copyright (C) 2018, Mikel Artetxe

Licensed under the terms of the GNU General Public License, either version 3 or (at your option) any later version. A full copy of the license can be found in LICENSE.txt.
