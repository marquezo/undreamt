import argparse
import io
import numpy as np
import tqdm


def load_vec(emb_path, nmax=70000):
    vectors = []
    word2id = {}

    with io.open(emb_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
        next(f)
        for i, line in enumerate(f):
            word, vect = line.rstrip().split(' ', 1)
            vect = np.fromstring(vect, sep=' ')
            assert word not in word2id, 'word found twice'
            vectors.append(vect)
            word2id[word] = len(word2id)

            if len(word2id) == nmax:
                break

    id2word = {v: k for k, v in word2id.items()}
    embeddings = np.vstack(vectors)

    return embeddings, id2word, word2id


def get_nn(word, src_emb, src_id2word, tgt_embeddings, tgt_id2word):
    word2id = {v: k for k, v in src_id2word.items()}
    word_emb = src_emb[word2id[word]]
    scores = (tgt_embeddings / np.linalg.norm(tgt_embeddings, 2, 1)[:, None]).dot(word_emb / np.linalg.norm(word_emb))
    k_best = scores.argsort()[-1:][::-1][0]

    return tgt_id2word[k_best]


def main():

    parser = argparse.ArgumentParser(description="Translate using baseline")
    parser.add_argument("file", help="File containing the source sentences")
    parser.add_argument("src_emb")
    parser.add_argument("trg_emb")
    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf8') as file:
        lines = file.readlines()

    src_embeddings, src_id2word, src_word2id = load_vec(args.src_emb)
    trg_embeddings, trg_id2word, trg_word2id = load_vec(args.trg_emb)

    for line in tqdm.tqdm(lines):
        tokens = line.rstrip().split()
        result = []

        for token in tokens:
            if token in src_word2id:
                nn = get_nn(token, src_embeddings, src_id2word, trg_embeddings, trg_id2word)
                result.append(nn)
            else:
                result.append("<OOV>")

        print(" ".join(result))


if __name__ == '__main__':
    main()