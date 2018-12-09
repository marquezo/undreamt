Trying out Artetxe's [UNdreaMT](https://github.com/artetxem/undreamt) on English-Basque
==================

The goal is to see whether Artetxe's method works on a low-resource pair such as English-Basque, in particular if we can do better than the results reported in ["English-Basque Statistical and Neural Machine Translation"](http://www.lrec-conf.org/proceedings/lrec2018/pdf/101.pdf) where they only trained with about 130,000 phrase pairs (small dataset).

* Basque monolingual embeddings taken from https://fasttext.cc/docs/en/pretrained-vectors.html
* English monolingual embeddings taken from https://fasttext.cc/docs/en/english-vectors.html

Results of vecmap on English-Basque on 30 pairs (test_dict.txt)
-------------

| Method          | Coverage   | Accuracy - NN  | Accuracy - CSLS  |
| ----------------|:----------:| --------------:| ----------------:|
| Unsupervised    | 96.67%     | 0%             | 0%               | 
| Seed = 27 pairs | 96.67%     | 37.93%         | 31.03%           | 
| Seed = 101 pairs| 96.67%     | 41.38%         | 37.93%           | 



Requirements
--------
- Python 3
- PyTorch (tested with v0.3)
- NLTK
- tqdm
- Also, need to do:
  `import nltk`
  `nltk.download('punkt')`

Order of pre-processing should be:

* `bash prep_eu_wiki.sh`
* `bash prep_en_data.sh`
* `bash download_embeddings.sh`
* `python extract_vocab.py cc.eu.300.vec vocab.eu train_vocab.eu`
* `python extract_vocab.py wiki-news-300d-1M.vec vocab.en train_vocab.en`

No need to do the following two steps as Artetxe's code uses "OOV" if token is not in supplied vocab
* `python update_corpus.py sentences.en train_vocab.en train_sentences.en`
* `python update_corpus.py sentences.eu train_vocab.eu train_sentences.eu`

Then to use [vecmap](https://github.com/artetxem/vecmap) we need to git clone it and then something like:

* `cd vecmap`
* `nohup python3 map_embeddings.py --semi_supervised ../undreamt/train_dict.txt ../undreamt/train_vocab.en ../undreamt/train_vocab.eu ../undreamt/train_emb_mapped.en ../undreamt/train_emb_mapped.eu > out.log &`

Evaluation data was taken from https://github.com/ijauregiCMCRC/english_basque_MT
