import argparse
import numpy as np


# Filter sentences according to length of source
def filter_sentences(src_sents, trg_sents, min_tokens, max_tokens):
    src_to_return = []
    trg_to_return = []

    for idx, sent in enumerate(src_sents):

        if min_tokens <= len(sent.split()) <= max_tokens:
            src_to_return.append(sent)
            trg_to_return.append(trg_sents[idx])

    return src_to_return, trg_to_return


def main():
    parser = argparse.ArgumentParser(description="Given two parallel corpora already tokenized, split in train, valid and test sets")
    parser.add_argument("src_sentences", help="Source sentences", type=str)
    parser.add_argument("trg_sentences", help="Target sentences", type=str)
    parser.add_argument("--min_tokens", help="Minimum number of tokens per sentence in the source", type=int, default=3)
    parser.add_argument("--max_tokens", help="Maximum number of tokens per sentence in the source", type=int, default=50)
    parser.add_argument("--size_valid_test", help="Size of valid and test sets", type=int, default=5000)

    args = parser.parse_args()

    with open(args.src_sentences, mode='rt', encoding='utf-8') as file_s:
        src_sentences = file_s.readlines()

    with open(args.trg_sentences, mode='rt', encoding='utf-8') as file_t:
        trg_sentences = file_t.readlines()

    src_sentences, trg_sentences = filter_sentences(src_sentences, trg_sentences, args.min_tokens, args.max_tokens)

    num_sents = len(src_sentences)

    shuffled = list(np.random.choice(num_sents, num_sents, replace=False))
    train_idx = shuffled[:num_sents - args.size_valid_test*2]
    valid_idx = shuffled[num_sents - args.size_valid_test*2: num_sents - args.size_valid_test]
    test_idx = shuffled[num_sents - args.size_valid_test:]

    with open(args.src_sentences + ".train", 'w') as file:
        file.writelines("%s" % src_sentences[idx] for idx in train_idx)

    with open(args.trg_sentences + ".train", 'w') as file:
        file.writelines("%s" % trg_sentences[idx] for idx in train_idx)

    with open(args.src_sentences + ".valid", 'w') as file:
        file.writelines("%s" % src_sentences[idx] for idx in valid_idx)

    with open(args.trg_sentences + ".valid", 'w') as file:
        file.writelines("%s" % trg_sentences[idx] for idx in valid_idx)

    with open(args.src_sentences + ".test", 'w') as file:
        file.writelines("%s" % src_sentences[idx] for idx in test_idx)

    with open(args.trg_sentences + ".test", 'w') as file:
        file.writelines("%s" % trg_sentences[idx] for idx in test_idx)


if __name__ == "__main__":
    main()
