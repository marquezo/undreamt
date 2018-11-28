#!/bin/bash

wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/word-vectors-v2/cc.eu.300.vec.gz
wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki-news-300d-1M.vec.zip
gunzip cc.eu.300.vec.gz
python extract_zip.py wiki-news-300d-1M.vec
