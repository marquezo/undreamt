#! /usr/bin/python
"""
BLEU score assessor
"""
# -*- coding: utf-8 -*-
import argparse
from unicodedata import normalize
import re, string
from euskalToken import EuskalToken
from nltk.tokenize.treebank import TreebankWordTokenizer


def main():

    parser = argparse.ArgumentParser(description="Tokenize sentences")
    parser.add_argument("file", help="Ground truth filename")
    parser.add_argument("lang", choices=['en', 'eu'])
    args = parser.parse_args()

    word_tokenizer = EuskalToken() if args.lang == 'eu' else TreebankWordTokenizer()
    # prepare regex for char filtering
    re_print = re.compile('[^%s]' % re.escape(string.printable))

    with open(args.file, 'r', encoding='utf8') as file:
        lines = file.readlines()

        for line in lines:
            line = line.rstrip()
            # normalize unicode characters
            line = normalize('NFD', line).encode('ascii', 'ignore')
            line = line.decode('UTF-8')
            # tokenize
            line = word_tokenizer.tokenize(line)
            # convert to lower case
            line = [word.lower() for word in line]
            # remove non-printable chars from each token
            line = [re_print.sub('', w) for w in line]
            print(" ".join(line))


if __name__ == '__main__':
    main()
