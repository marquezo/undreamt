#!/bin/bash

wget http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2013.en.shuffled.gz
gunzip news.2013.en.shuffled.gz
python preprocess_corpus.py news.2013.en.shuffled vocab.en sentences.en en
