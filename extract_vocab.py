import argparse
import io


def main():
    parser = argparse.ArgumentParser(description="Extract the word embeddings for a given vocabulary")
    parser.add_argument("embeddings", help="File containing the word embeddings in text format", type=str)
    parser.add_argument("vocab", help="File containing the vocabulary", type=str)
    parser.add_argument("output_embeddings", help="File to store the embeddings for the given vocabulary", type=str)

    args = parser.parse_args()

    input_embs = args.embeddings
    vocab_file = args.vocab
    output_embs = args.output_embeddings

    with open(vocab_file, "r") as file:
        vocab = [token.rstrip() for token in file.readlines()]

    embeddings_handler = io.open(input_embs, 'r', encoding='utf-8', newline='\n', errors='ignore')

    n, d = map(int, embeddings_handler.readline().split())
    print("Found {} embeddings with dimension {}".format(n, d))

    data = {}

    for line in embeddings_handler:
        tokens = line.rstrip().split(' ')

        if tokens[0] in vocab:
            data[tokens[0]] = tokens[1:]

    with open(output_embs, 'w') as file:
        file.write("{} {}\n".format(len(data), d))

        for k, v in data.items():
            file.write("{} {}\n".format(k, " ".join(v)))

    print("Finished writing embeddings containing {} tokens".format(len(data)))


if __name__ == "__main__":
    main()
