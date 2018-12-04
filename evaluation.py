#! /usr/bin/python
"""
BLEU score assessor
"""
# -*- coding: utf-8 -*-
import argparse
import numpy as np
from euskalToken import EuskalToken
from nltk.translate import bleu_score


def avg_of_sentence_bleu_scores(groundtruth_filename, prediction_filename):
    
    list_of_scores = []
    basque_tokenizer = EuskalToken()
    
    with open(groundtruth_filename, encoding="utf8") as gtfile, open(prediction_filename, encoding="utf8") as predfile:
   
        for i, (gt_sentence, predicted_sentence) in enumerate(zip(gtfile, predfile)):   
            gt_list_of_tokens = basque_tokenizer.tokenize(gt_sentence)
            predicted_list_of_tokens = predicted_sentence.split()

            list_of_scores.append(bleu_score.sentence_bleu([gt_list_of_tokens], predicted_list_of_tokens))
            
        array_of_scores = np.asarray(list_of_scores)
        avg_bleu_scores = array_of_scores.mean()
          
    return avg_bleu_scores


def main():

    parser = argparse.ArgumentParser(description="Sentence-BLEU score assessor for paralleled sentences")
    parser.add_argument("gd_filename", help="Ground truth filename")
    parser.add_argument("pred_filename", help="Prediction filename")
    args = parser.parse_args()

    score = avg_of_sentence_bleu_scores(args.gd_filename, args.pred_filename)

    print("Non smoothed BLEU score: %f" % (score*100))


if __name__ == '__main__':
    main()
