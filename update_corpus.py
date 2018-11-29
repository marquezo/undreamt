import argparse
import concurrent.futures
from itertools import repeat
import math


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# mark all OOV with "unk" for all lines
def update_dataset(lines, vocab, unk_token='<UNK>'):
    new_lines = []

    for line in lines:
        new_tokens = []

        for token in line.split():
            if token in vocab:
                new_tokens.append(token)
            else:
                new_tokens.append(unk_token)

        new_line = ' '.join(new_tokens)
        new_lines.append(new_line)

    return new_lines


def process_corpus(corpus, vocab_file):

    with open(corpus, mode='rt', encoding='utf-8')as file:
        sentences = file.readlines()

    with open(vocab_file, 'r') as file:
        vocab = [line.rstrip().split()[0] for line in file.readlines()]

    print("Updating dataset")
    updated_sentences = []

    # Break into 1000 chunks
    num_chunks = 1000
    chunked_sentences = chunks(sentences, num_chunks)
    vocab_repeated = repeat(vocab, math.ceil(len(sentences)/num_chunks))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for updated_sents in executor.map(update_dataset, chunked_sentences, vocab_repeated):
            updated_sentences.extend(updated_sents)

            if len(updated_sentences) % 10000 == 0:
                print("Processed {} sentences".format(len(updated_sentences)))

    return updated_sentences


def main():
    parser = argparse.ArgumentParser(description="Given a corpus and a vocab, replace tokens not in vocab with <UNK>")
    parser.add_argument("corpus", help="Corpus that will be updated given the vocabulary", type=str)
    parser.add_argument("vocab", help="Vocabulary in text embeddings format", type=str)
    parser.add_argument("sentences", help="File where to output the pre-processed sentences", type=str)

    args = parser.parse_args()

    corpus = args.corpus
    vocab_file = args.vocab
    output_file = args.sentences

    sentences = process_corpus(corpus, vocab_file)

    with open(output_file, 'w') as file:
        file.writelines("%s\n" % line for line in sentences)


if __name__ == "__main__":
    main()
