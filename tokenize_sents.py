#! /usr/bin/python
"""
BLEU score assessor
"""
# -*- coding: utf-8 -*-
import argparse
from euskalToken import EuskalToken
from nltk.tokenize.treebank import TreebankWordTokenizer


def avg_of_sentence_bleu_scores(groundtruth_filename, prediction_filename):
    
    list_of_scores = []
    basque_tokenizer = EuskalToken()
    
    with open(groundtruth_filename, encoding="utf8") as gtfile, open(prediction_filename, encoding="utf8") as predfile:
   
        for i, (gt_sentence, predicted_sentence) in enumerate(zip(gtfile, predfile)):   
            gt_list_of_tokens = basque_tokenizer.tokenize(gt_sentence)
            predicted_list_of_tokens = predicted_sentence.split()
            print(gt_list_of_tokens)
            print(predicted_list_of_tokens)
            score = bleu_score.sentence_bleu([gt_list_of_tokens], predicted_list_of_tokens)
            list_of_scores.append(score)
            print(score)
            
        array_of_scores = np.asarray(list_of_scores)
        avg_bleu_scores = array_of_scores.mean()
          
    return avg_bleu_scores


def main():

    parser = argparse.ArgumentParser(description="Tokenize sentences")
    parser.add_argument("file", help="Ground truth filename")
    parser.add_argument("lang", choices=['en', 'eu'])
    args = parser.parse_args()

    word_tokenizer = EuskalToken() if args.lang == 'eu' else TreebankWordTokenizer()

    with open(args.file, 'r', encoding='utf8') as file:
        lines = file.readlines()

        for line in lines:
            tokens = word_tokenizer.tokenize(line.rstrip())
            print(" ".join(tokens))


if __name__ == '__main__':
    main()
